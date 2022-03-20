<h1>ScreeManager</h1>
<p>ScreenManager is a small tool for pygame, for creating scenes and managing them.
It was made in order to facilitate this process, which many (especially those who
is starting in the library).</p>

> [!OBS] A partir de agora, quando falar 'Screen', estarei me referindo as Cenas.

 - [ScreenManager](#screemanager)
      * [update](#_update_)
      * [external_screen_events](#_external_screen_events_)
      * [change_current](#_change_current_)
      * [add_screen](#_add_screen_)
 - [Screen](#screen)
      * [update](#update)
      * [on_evet](#_on_event_)
      * [on_pre_enter](#_on_pre_enter_)
      * [on_enter](#_on_enter_)
      * [on_pre_exit](#_on_pre_exit_)
      * [on_exit](#_on_exit_)

<h2>Basic use</h2>
<p>To create a Screen, of course, you must create a basic structure of a project
with pygame.</p>

````python
# create the main project cycle:
import pygame

pygame.init()

version = '1.0.0'

# create a main surface:
display = pygame.display.set_mode([500, 320])
pygame.display.set_caption(f'screen teste - {version}')

running = True

while running:
    # create a variable for events:
    events = pygame.event.get()

    # create the event loop
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            
    pygame.display.update()
````
With a base structure created, now import ``Screen`` and ``ScreenManager``
and instantiate ``ScreenManager()`` to a variable. In ``ScreenManager()`` pass the
``display`` variable as a parameter.

````
sm = ScreenManager(display)
````

Now declare the classes for each Screen you want to create and pass ``Screen`` as
``metaclass``, and in each class define the ``update()`` and ``on_event()`` methods.
>[!WARMING] If one of the mentioned methods is not defined, it will generate a ``TypeError``
>, as they are the ``abstractmethod`` of the ``Abstract Base Classes`` ``Screen()``

````python
# create a class for the first screen:
class Screen1(Screen):
    # set the update method
    def update(self, _events):
        pygame.draw.rect(self.surface, [255, 255, 255], [50, 90, 90, 90])
        pygame.draw.rect(self.surface, [255, 255, 255], [50, 200, 90, 90])
        
    # define the on_event method:
    def on_event(self, _event):
        pass


class Screen2(Screen):
    # set the update method
    def update(self, _events):
        pygame.draw.rect(self.surface, [255, 255, 255], [200, 95, 100, 100])

    # define the on_event method:
    def on_event(self, _event):
        pass
````
To change Screens I will use the `pygame.K_SPACE` key, the `_event` parameter
will be responsible for catching the event, follow the code.

**switch to Screen2 screen:**
````python
def on_event(self, _event):
    if _event.type == pygame.KEYDOWN:
        # once SPACE key is pressed change the current screen to the defined target.
        if _event.key == pygame.K_SPACE:
            sm.change_current('screen2')
````
**switch to Screen1 screen:**
````python
def on_event(self, _event):
    if _event.type == pygame.KEYDOWN:
        # once SPACE key is pressed change the current screen to the defined target.
        if _event.key == pygame.K_SPACE:
            sm.change_current('screen1')
````

After these steps add the Screens with the `ScreenManager().add_screen()` method.

````python
sm.add_screen(Screen1(sm.surface))
sm.add_screen(Screen2(sm.surface))
````
And finally call `update()` from `ScreenManager()` in the main loop. pass to
`events` variable as a parameter.

````python
sm.update()
````

**full code:**
````python
import pygame
from pgtools.screenmanager import Screen, ScreenManager

pygame.init()

version = '1.0.0'

# create a main surface:
display = pygame.display.set_mode([500, 320])
pygame.display.set_caption(f'screen teste - {version}')


# create a class for the first screen:
class Screen1(Screen):
    # set the update method
    def update(self, _events):
        pygame.draw.rect(self.surface, [255, 255, 255], [50, 90, 90, 90])
        pygame.draw.rect(self.surface, [255, 255, 255], [50, 200, 90, 90])
        
    # define the on_event method:
    def on_event(self, _event):
        if _event.type == pygame.KEYDOWN:
            # once SPACE key is pressed change the current screen to the defined target.
            if _event.key == pygame.K_SPACE:
                sm.change_current('screen2')


class Screen2(Screen):
    # set the update method
    def update(self, _events):
        pygame.draw.rect(self.surface, [255, 255, 255], [200, 95, 100, 100])

    # define the on_event method:
    def on_event(self, _event):
        if _event.type == pygame.KEYDOWN:
            # once SPACE key is pressed change the current screen to the defined target.
            if _event.key == pygame.K_SPACE:
                sm.change_current('screen1')


sm = ScreenManager(display)

sm.add_screen(Screen1(sm.surface))
sm.add_screen(Screen2(sm.surface))

running = True

while running:
    # create a variable for events:
    events = pygame.event.get()

    # create the event loop
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
    sm.update(events)
    pygame.display.update()
````

<h2>Reference</h2>

<h2>ScreenManager:</h2>

````python
from pgtools.screenmanager import ScreenManager
````

The ScreenManager, as the name implies, is the screen manager of the project,
this is where it all happens, for each project there must be only one manager. For
to use it simply instantiate the `ScreeManager()` class to a variable, pass
`pygame.display.set_mode()` as a parameter.

````python
display = pygame.display.set_mode([650, 300])
manager = ScreenManager(display)
````

And after that call the `update()` method in the main cycle of the project, from the
manager variable, in this case `manager`, in `update()` pass `pygame.event.get()`
as a parameter, and the rest he will do.

````python
[...]

manager.internal_cycle_events = False

running = True

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
            
        manager.external_screen_events(event)
    
    # update method
    manager.update(events)
    pygame.display.update()
````

<h2>Class attributes</h2>

| **name** 	| **type** 	| **default value** 	| **description** 	|
|:---:	|:---:	|---	|:---:	|
| `surface` 	| `pygame.Surface` 	| parameter `surface` 	| surface where all screens will be drawn 	|
| `current` 	| `screenmanager.Screen` 	| fist `Screen` added 	| Current screen, at runtime 	|
| `internal_cycle_events` 	| `boolean` 	| `True` 	| if set to `True` it will create an event loop internally in the handler, without the need to make any direct calls to the main event loop of the project. If it is `False`, for the events to be verified, it is necessary to make a direct call of the events in the main event cycle of the project with the method [SreenManager().external_screen_events()](#external_screen_events) 	|
| `starts_first_screen` 	| `boolean` 	| `True` 	| if the first screen to be shown in the window is the first one added in the manager 	|

<h2>Method's:</h2>

<h3>_update_</h3>

````
ScreenManager().update()
````

Method responsible for updating all Screens. Like any "update" method in
pygame the ScreenManager `update()` must be called in the main project cycle
for the Screens to be updated.

````python
[...]

while running:
    events = pygame.event.get()
    for event in events:
        [...]
    
    # update method
    sm.update(events)
    
    [...]
````

**parameters**

| **name** 	| **type** 	| **default value** 	| **description** 	|
|:---:	|:---:	|---	|:---:	|
| `events_get` 	| `pygame event` 	| undefined 	| The events, use `pygame.event.get()` this is necessary if you want to use other plug-ins like [pygame_widgets](https://pygamewidgets.readthedocs.io/en/latest/), besides that you will need the parameter if you want to make use of the event cycle created by the manager itself 	|

-- -
<h3>_external_screen_events_</h3>

````
SreenManager().external_screen_events()
````

Method responsible for creating the private events between the Screens, because in case
the events of each Screen is in the `events` loop (this loop
`for event in pygame.event.get(): [...]`) may conflict between them,
For example, when pressing the Space key on the keyboard, a character jumps on the screen, while in the menu the same key is used for another function, thus executing two functions at the same time, and so that it does not
If conflicts like this happen, `external_screen_events()` was created.

>[!TIP] always use this method when `SreenManager().internal_screen_events = False`
> thus requiring less processing as the events will not be in an internal loop
> while the events are already being executed by the `external_screen_events()` method

````python
[...]

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: [...]
        
        sm.external_screen_events(event)

    [...]
````

**parameters**

| **name** 	| **type** 	| **default value** 	| **description** 	|
|:---:	|:---:	|---	|:---:	|
| `_event` 	| `pygame event` 	| undefined 	| parameter responsible for catching each event of the `for` loop 	|

-- -

<h3>_add_screen_</h3>

````
ScreenManager().add_screen()
````

Use it to add Screens. If `starts_first_screen = True` so
added to the first Screen it will be saved as `current` ie when the window
start will be the first to be drawn on the display.

````python
sm = ScreenManager(display)

sm.add_screen(Menu(sm.surface))
sm.add_screen(Game(sm.surface))
sm.add_screen(Settings(sm.surface))
````

**parameter**

| **name** 	| **type** 	| **default value** 	| **description** 	|
|:---:	|:---:	|---	|:---:	|
| `target` 	| `screenmanager.Screen` 	| undefined 	| target class to add as Screen 	|

-- -

<h3>_change_current_</h3>

````
ScreenManager().change_current()
````

To make the Screen transition use it, in case you change from Screen manually by changing
the value of the `current` attribute will not execute the output and input procedures
from Screen.

````python
[...]

if event.key == pygame.K_SPACE:
    sm.change_current('game')
    
[...]
````

**parameter**

| **name** 	| **type** 	| **default value** 	| **description** 	|
|:---:	|:---:	|---	|:---:	|
| `target` 	| `str` 	| undefined 	| target Screen name to be new current 	|

-- -

<h2>Screen</h2>

````python
from pgtools.screenmanager import Screen
````

Screen is just an `Abstract Base Classes`, where all screens must be
based. classes are identified by the manager by class name
in lower case so if you declare a class with the name "Menu", its name
will be "menu", it's important to know this when making transitions
of screens.

>[!IMPORTANT] whenever you want to draw something on your Screen you should use the attribute
> `Screen();surface`, otherwise if you draw things using the root surface
> of the project, it will be drawn, but under the current Screen.

<h3>Example</h3>

````python
class Menu(Screen):
    def update(self, _events):
        pygame.draw.rect(self.surface, [255, 255, 255], [50, 50, 100, 100])
        
    def on_event(self, _event):
        pass
````

<h3>Method's</h3>:

<h3>update</h3>

````python
def update(self, _events):
    [...]
````

Everything you want to update on Screen must be in this method, it works
as if it were the main cycle of the project itself, only the content will be updated
of the Screen set to current.

**parameter:**

| **name** 	| **type** 	| **default value** 	| **description** 	|
|:---:	|:---:	|---	|:---:	|
| `_events` 	| `pygame events` 	| undefined 	| it's just to have compatibility with the [pygame widgets](https://pygamewidgets.readthedocs.io/en/latest/) library, as some elements of the library need a certain parameter. 	|

-- -

<h3>_on_event_</h3>

````python
def on_event(self, _event):
    [...]
````

Simulate the event loop, use the `_event` parameter as the event loop variable
main project events.

**parameter:**

| **name** 	| **type** 	| **default value** 	| **description** 	|
|:---:	|:---:	|---	|:---:	|
| `_event` 	| `pygame event` 	| undefined 	| works as the project's main event loop event variable 	|

-- -

<h3>_on_enter_</h3>
````python
def on_enter(self):
    [...]
````

Called upon entering Screen

-- -

<h3>_on_pre_enter_</h3>

````python
def on_pre_enter(self):
    [...]
````

Called before entering the Screen

-- -

<h3>_on_exit_</h3>

````python
def on_exit(self):
    [...]
````

Called when exiting Screen

-- -

<h3>_on_pre_exit_</h3>

````python
def on_pre_exit(self):
    [...]
````

Called before leaving Screen.
