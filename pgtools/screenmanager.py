from abc import ABC, abstractmethod

import pygame

'''
    This is the module that will do whatever it takes to create your screens, it is required that
you have pygame installed to work correctly.

    All your screens must be a class that inherits Screen().
    
    The ScreenManager class must be called only outside the project's main loop, and it is mandatory
that ScreenManager().update() is called inside the project's main loop, so that everything works correctly.

    In Screen(), the methods: on_event() and update() are mandatory.
'''


class ScreenManager:
    def __init__(self, surface):
        """
            A screen manager, for all screens to work, this class must be called.

            [OBS] the screen manager must be called outside the main project cycle,
        where all your screens will be added.

        :param surface: Use pygame.display.set_mode(), the main project surface.
        """

        self.surface = surface

        # where the screens will be stored.
        self.__screens = {}

        # what screen is being displayed.
        self.current = ''

        # defines whether the event cycles must be internal of the managed or external,
        # the main event cycle of the project.
        self.internal_cycle_events = True

        # define whether to start with the first screen to be added
        self.starts_first_screen = True
        self.__no_screens = True

        # call control for some screen methods.
        self.__call_control = {
            'on_enter': True,
            'on_pre_enter': True
        }

    def update(self, events_get):
        """
            Method responsible for keeping the updates of each screen, in addition to triggering
        events if self.internal_cycle_events is True.

            [OBS] This method should only be called within the main project cycle.

        :param events_get:
        """

        current: Screen = self.__screens[self.current]

        # checks if events are internal.
        if self.internal_cycle_events:
            self.__internal_screen_events__(events_get)

        # check if you are entering the current screen.
        if self.__call_control['on_pre_enter']:
            self.__call_control['on_pre_enter'] = False
            current.on_pre_enter()

        # here is calling the methods responsible for rendering and updating the current screen.
        self.surface.blit(current.surface, (0, 0))
        current.update(events_get)

        # checks if the screen has started.
        if self.__call_control['on_enter']:
            self.__call_control['on_enter'] = False
            current.on_enter()

    def external_screen_events(self, _event):
        """
            The function of this method is to create a private 'sandbox' of events, thus without having
        any changes in other screens.

            The advantage of using this method in particular, than using the built-in 'sandbox' created
        by the manager itself of screens, is that it will be called directly in the main event cycle, thus
        improving the project performance.

            [OBS] This method must be called within the main event cycle of the project.

        :param _event: must be the events variable of the main event loop
                     'for event in pygame.event.get()'
                          ↑ ↑ ↑
                      this variable
        """
        self.__screens[self.current].on_event(_event)

    def add_screen(self, target):
        """
            Method responsible for adding new screens, for the ScreenManager to work correctly,
        at least one screen must be added, the screen that starts first in the project window
        will be the first to be added.

        :param target: Target class to be added.

        :type target: Must receive a class with a Screen() meta class.
        """

        # checks whether to start with the first screen added or start with the last one
        if self.starts_first_screen:
            if self.__no_screens:
                self.__no_screens = False
                self.current = target.name
        else:
            self.current = target.name

        # add the class in question to one in a dictionary
        self.__screens[target.name] = target

    def change_current(self, target):
        """
            Method responsible for making screen transitions, and executing some methods during the action.

        :param target: target screen that will be changed to current.
        """

        # reset call control.
        self.__call_control['on_enter'] = True
        self.__call_control['on_pre_enter'] = True

        # calling procedures before the screen is closed.
        self.__screens[self.current].on_pre_exit()

        old_current = self.current

        # changing screen.
        self.current = target

        # calling procedures after the current old one has closed.
        self.__screens[old_current].on_exit()

    def __internal_screen_events__(self, __events):

        # internal private event loop
        for _event in __events:
            self.__screens[self.current].on_event(_event)


class Screen(ABC):
    def __init__(self, surface):
        """ An abstracted base class where all your screens are based. """

        # default screen name, based on lowercase class name.
        self.name = self.__class__.__name__.lower()

        # defining her surface and her size.
        self.surface = pygame.Surface(surface.get_size())

    @abstractmethod
    def update(self, _events):
        """
            Here will be all the updates of your screen, it will be called in the main cycle of the project
        by ScreenManager().update() if it is the current screen.

            If you need to associate some event you can use the _events parameter for this task.
        """
        ...

    @abstractmethod
    def on_event(self, _event):
        """
            Similar to the update() method, this method is called in the main project cycle, where it can be
        called by a Managed private sandbox or in the project's main event cycle.

            The events will be associated with the _events parameter, so if you want to create a private event
        within the sandbox of your screen, it will do this task.
        """
        ...

    def on_enter(self):
        """ Put here everything you wanted to be executed after entering the screen in question. """
        ...

    def on_pre_enter(self):
        """ Put here everything you wanted to be executed before entering the screen in question. """
        ...

    def on_exit(self):
        """ Put here everything you wanted to be executed after leaving the screen in question. """
        ...

    def on_pre_exit(self):
        """ Put here everything you wanted to be executed before leaving the screen in question. """
        ...


if __name__ == '__main__':
    """ example of how to create screens. """

    pygame.init()

    # create a main surface:
    display = pygame.display.set_mode([500, 320])
    pygame.display.set_caption('screen test')

    # define a managed, and set the canvas as default surface:
    sm = ScreenManager(display)

    # create a class for the first screen:
    class Screen1(Screen):
        def __init__(self, surface):
            super().__init__(surface)

        # set the update method
        def update(self, _events):
            # the surface to be drawn is the screen surface, which is the value of self.surface
            #
            #                  surface
            #                  ↓ ↓ ↓ ↓
            pygame.draw.rect(self.surface, [255, 255, 255], [50, 90, 90, 90])

            pygame.draw.rect(self.surface, [255, 255, 255], [50, 200, 90, 90])

        # define the on_event method:
        def on_event(self, _event):
            if _event.type == pygame.KEYDOWN:

                # once SPACE key is pressed change the current screen to the defined target.
                if _event.key == pygame.K_SPACE:
                    sm.change_current('screen2')

        # as soon as it exits it will print the content:
        def on_exit(self):
            print('it went out')


    class Screen2(Screen):
        def __init__(self, surface):
            super().__init__(surface)

        # set the update method
        def update(self, _events):
            # the surface to be drawn is the screen surface, which is the value of self.surface
            #
            #                  surface
            #                  ↓ ↓ ↓ ↓
            pygame.draw.rect(self.surface, [255, 255, 255], [200, 95, 100, 100])

        # define the on_event method:
        def on_event(self, _event):
            if _event.type == pygame.KEYDOWN:

                # once SPACE key is pressed change the current screen to the defined target.
                if _event.key == pygame.K_SPACE:
                    sm.change_current('screen1')

        # before entering will print entering
        def on_pre_enter(self):
            print('entering')

    # add to the screens in the manager and it must be passed in.surface as a parameter:
    # obs: as screen1 was added first, it will be the screen that will be initialized along with the display.
    sm.add_screen(Screen1(sm.surface))
    sm.add_screen(Screen2(sm.surface))

    # disabling the manager's built-in event loops:
    sm.internal_cycle_events = False

    # create the main project cycle:
    running = True

    while running:
        # create a variable for events:
        events = pygame.event.get()

        # create the event loop
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            # as it was set sm.internal_cycle_events to False it will be necessary to add this method:
            # event must be passed as parameter.
            sm.external_screen_events(event)

        # updating the manager:
        sm.update(events)

        pygame.display.update()
