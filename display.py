from typing import Optional
from support import *

# Display helper components, you can probably ignore these ---------------------
class DisplayError(Exception): ... # Custom error so as not to trigger excepts

class TextDisplayElement():
    """
    Base (Abstract) text gui element to display a rectangular block of text.
    Display works based on list of strings. String represents the content of a 
    row (top to bottom). The render method returns the block of text to display 
    this element. content will be justified so it is always the width and height
    specified by get_width and get_height respectively. If width and height
    are not specified, then width and height stretch to the longest column/row
    respectively. The display method prints render content. 

    The intention is for TextDisplayElement child classes to nest one-another
    in order to more easily lay out a text based GUI. This generally should be 
    achieved by the render method of an encompassing element calling the render 
    element of its nested elements before stitching the resulting content 
    together, calling its own justify method on the result, and returning.

    This class should not be instantiated directly, and should instead be 
    subclassed. Subclasses should override the render method with intended 
    functionality.
    """

    # Justification settings
    VJUST_TOP = "top"
    VJUST_BOTTOM = "bottom"
    VJUST_CENTER = "center" #if even sides left
    HJUST_LEFT = "left"
    HJUST_RIGHT = "right"
    HJUST_CENTER = VJUST_CENTER # if even sides top

    def __init__(self, 
                 width: Optional[int] = None, 
                 height: Optional[int] = None,
                 vjust: str = VJUST_CENTER,
                 hjust: str = HJUST_CENTER
    ):
        """
        Initialises a new TextDisplayElement.

        Args:
            width (Optional[int], optional): Fixed width, or None to stretch to 
                                             widest row. Defaults to None.
            height (Optional[int], optional): Fixed height, or None to stretch 
                                              to number of rows in content. 
                                              Defaults to None.
            vjust (str, optional): Vertical content justification.
                                   Can either be "top", "bottom" or "center". 
                                   Defaults to "center".
            hjust (str, optional): Horizontal content justification. 
                                   Can either be "left", "right" or "center".
                                   Defaults to "center".
        """
        self._fixwidth = width
        self._fixheight = height

        self.set_vjust(vjust)
        self.set_hjust(hjust)

    def set_width(self, width: Optional[int] = None):
        """
        Set or remove fixed width. Removing fixed width means width stretches to
        widest row.

        Args:
            width (Optional[int], optional): New fixed width, or None to remove 
                                             fixed width. Defaults to None.
        """
        self._fixwidth = width

    def get_width(self) -> int:
        """
        Returns current content width.

        Returns:
            int: current content width.
        """
        if self._fixwidth:
            return self._fixwidth
        else:
            return max((len(row) for row in self._content), default= 0)
    
    def set_height(self, height: Optional[int] = None):
        """
        Set or remove fixed height. Removing fixed height means height stretches 
        to number of content rows.

        Args:
            height (Optional[int], optional): New fixed height, or None to 
                                              remove fixed height. Defaults to 
                                              None.
        """
        self._fixheight = height

    def get_height(self) -> int:
        """
        Returns current content height.

        Returns:
            int: current content height.
        """
        if self._fixheight:
            return self._fixheight
        else:
            return len(self._content)
        
    def set_vjust(self, vjust: str):
        if vjust not in (self.VJUST_TOP, self.VJUST_CENTER, self.VJUST_BOTTOM):
            raise DisplayError("invalid vertical justification, please use "+ 
                             f"'{self.VJUST_TOP}', " +
                             f"'{self.VJUST_CENTER}', or " +
                             f"'{self.VJUST_BOTTOM}'"
            )
        self._vjust = vjust

    def set_hjust(self, hjust: str):
        if hjust not in (self.HJUST_LEFT, self.HJUST_CENTER, self.HJUST_RIGHT):
            raise DisplayError("invalid horizontal justification, please use "+ 
                             f"'{self.HJUST_LEFT}', " +
                             f"'{self.HJUST_CENTER}', or " +
                             f"'{self.HJUST_RIGHT}'"
            )
        self._hjust = hjust
    
    def justify(self, content: list[str]) -> list[str]:
        """
        Return copy of given content padded such that it is rectangular with 
        the correct width and height. Content is justified according to the given
        justification settings.

        Args:
            content (list[str]): Content to pad/justifiy

        Raises:
            DisplayError: If content is too wide/tall for current fixed 
                          width/height

        Returns:
            list[str]: Padded and justified copy of given content.
        """
        # pad content horizonally
        to_render = []
        for line in content:
            hdiff = self.get_width() - len(line)
            if hdiff < 0:
                raise DisplayError("Content too wide!")
            if self._hjust == self.HJUST_LEFT:
                to_render.append(line + (" " * hdiff))
            elif self._hjust == self.HJUST_RIGHT:
                to_render.append((" " * hdiff) + line)
            elif self._hjust == self.HJUST_CENTER:
                lpad = hdiff // 2
                rpad = hdiff - lpad
                to_render.append((" " * lpad) + line + (" " * rpad))

        # pad content vertically
        vdiff = self.get_height() - len(to_render)
        if vdiff < 0:
            raise DisplayError("Content too tall!")
        if self._vjust == self.VJUST_TOP:
            to_render += [" " * self.get_width()] * vdiff
        elif self._vjust == self.VJUST_BOTTOM:
            to_render = ([" " * self.get_width()] * vdiff) + to_render
        elif self._vjust == self.VJUST_CENTER:
            tpad = vdiff // 2
            bpad = vdiff - tpad
            to_render = ([" " * self.get_width()] * tpad) + \
                    to_render + \
                    ([" " * self.get_width()] * bpad)
        
        return to_render
        
    def render(self) -> list[str]:
        """
        Return content that should be printed to display the content of this
        TextDisplayElement

        Returns:
            list[str]: Content to display. Each string in the given list is a 
                       row of content. The list is ordered with the first string 
                                       being the topmost row, and the last
                                       string being the bottommost.

        """
        return self.justify(self._content)
    
    def display(self):
        """
        Print this TextDisplayElement to the screen.
        """
        print(str(self))

    def __str__(self): # For easier debugging
        return "\n".join(self.render())

    def __repr__(self): # For even easier debugging (and because I am lazy)
        return str(self)


class BaseDisplay(TextDisplayElement):
    """
    Basic text display element. Takes manually specified content and displays it.
    """
    def __init__(self,
                 content: Optional[list[str]] = None, 
                 width: Optional[int] = None, 
                 height: Optional[int] = None, 
                 vjust: str = TextDisplayElement.VJUST_CENTER, 
                 hjust: str = TextDisplayElement.HJUST_CENTER
    ):
        """
        Initialises a BaseDisplay element.

        Args:
            content (Optional[list[str]], optional): content to display, 
                                                     or None for empty content. 
                                                     Defaults to None.
            width (Optional[int], optional): Fixed width, or None to stretch to 
                                             content. Defaults to None.
            height (Optional[int], optional): Fixed height, or None to stretch 
                                              to content. Defaults to None.
            vjust (str, optional): vertical justification setting. 
                                   Can either be "top", "bottom" or "center".
                                   Defaults to "center".
            hjust (str, optional): horizonatal justification setting.
                                   Can either be "left", "right" or "center". 
                                   Defaults to "center".
        """
        super().__init__(width, height, vjust, hjust)
        self._content = content if content else []

    def set_content(self, content: list[str]):
        """
        Set content to display.

        Args:
            content (list[str]): Content to display.
        """
        self._content = content

    def wrap_text(self, text: str) -> list[str]:
        """
        Attempts to break a given string into rows that would fit
        within this BaseDisplay element (breaking on spaces).
        Helpful for dispalying arbitrary content. This will behave weirdly
        without a set width.

        Args:
            text (str): String to break into lines

        Returns:
            list[str]: Content containing string broken into lines that should
                       Fit within this TextDisplay element.
        """
        wrapped = []
        remaining = text
        while len(remaining) > self.get_width():
            # find space to break on
            space = remaining.rfind(" ", 0, self.get_width())
            wrapped.append(remaining[0:space])
            remaining = remaining[space+1:]
            if space == -1:
                break # give up and deal with consequences later
        wrapped.append(remaining)
        return wrapped
        

class VSplitDisplay(TextDisplayElement):
    """
    TextDisplayElement that displays the content of several TextDisplayElements
    in a vertical stack (top to bottom). Can be indexed directly to access 
    contained TextDisplayElements.
    """
    def __init__(self, 
                 components: list[TextDisplayElement],
                 width: Optional[int] = None, 
                 height: Optional[int] = None, 
                 vjust: str = TextDisplayElement.VJUST_CENTER, 
                 hjust: str = TextDisplayElement.HJUST_CENTER
    ):
        """
        Initialises a new VSplitDisplayElement.

        Args:
            components (list[TextDisplayElement]): TextDisplayElements to 
                                                   display, ordered top to 
                                                   bottom.
            width (Optional[int], optional): Fixed width, or None to stretch to 
                                             content. Defaults to None.
            height (Optional[int], optional): Fixed height, or None to stretch 
                                              to content. Defaults to None.
            vjust (str, optional): vertical justification setting. 
                                   Can either be "top", "bottom" or "center".
                                   Defaults to "center".
            hjust (str, optional): horizonatal justification setting. 
                                   Can either be "left", "right" or "center".
                                   Defaults to "center".
        """
        super().__init__(width, height, vjust, hjust)
        self._components = components

    def components(self) -> list[TextDisplayElement]:
        """
        Return a reference to the list of displayed TextDisplayElements.

        Returns:
            list[TextDisplayElement]: displayed TextDisplayElements.
        """
        return self._components
    
    def __getitem__(self, index: int) -> TextDisplayElement:
        return self._components[index]

    def get_width(self) -> int:
        if self._fixwidth:
            return self._fixwidth
        else:
            return max((component.get_width() for component in self._components), default= 0)
        
    def get_height(self) -> int:
        if self._fixheight:
            return self._fixheight
        else:
            return sum((component.get_height() for component in self._components))

    def render(self):
        content_stack = []
        for component in self._components:
            content_stack += component.render()
        return self.justify(content_stack)
    

class HSplitDisplay(TextDisplayElement):
    """
    TextDisplayElement that displays the content of several TextDisplayElements
    in a horizontal stack (left to right). Can be indexed directly to access 
    contained TextDisplayElements.
    """
    def __init__(self, 
                 components: list[TextDisplayElement],
                 width: Optional[int] = None, 
                 height: Optional[int] = None, 
                 vjust: str = TextDisplayElement.VJUST_CENTER, 
                 hjust: str = TextDisplayElement.HJUST_CENTER
    ):
        """
        Initialises a new HSplitDisplayElement.

        Args:
            components (list[TextDisplayElement]): TextDisplayElements to 
                                                   display, ordered left to 
                                                   right.
            width (Optional[int], optional): Fixed width, or None to stretch to 
                                             content. Defaults to None.
            height (Optional[int], optional): Fixed height, or None to stretch 
                                              to content. Defaults to None.
            vjust (str, optional): vertical justification setting. 
                                   Can either be "top", "bottom" or "center".
                                   Defaults to "center".
            hjust (str, optional): horizonatal justification setting. 
                                   Can either be "left", "right" or "center".
                                   Defaults to "center".
        """
        super().__init__(width, height, vjust, hjust)
        self._components = components

    def components(self) -> list[TextDisplayElement]:
        """
        Return a reference to the list of displayed TextDisplayElements.

        Returns:
            list[TextDisplayElement]: displayed TextDisplayElements.
        """
        return self._components
    
    def __getitem__(self, index: int) -> TextDisplayElement:
        return self._components[index]
    
    def get_width(self) -> int:
        if self._fixwidth:
            return self._fixwidth
        else:
            return sum((component.get_width() for component in self._components))
        
    def get_height(self) -> int:
        if self._fixheight:
            return self._fixheight
        else:
            return max((component.get_height() for component in self._components), default= 0)

    def render(self):
        to_render = ["" for _ in range(self.get_height())]

        for component in self._components:
            new_content = component.render()
            # will need to pad vertically early
            vdiff = self.get_height() - len(new_content)
            if vdiff < 0:
                raise DisplayError("Component is too tall!")
            if self._vjust == self.VJUST_TOP:
                new_content += [" " * component.get_width()] * vdiff
            elif self._vjust == self.VJUST_BOTTOM:
                new_content = [" " * component.get_width()] * vdiff + new_content
            elif self._vjust == self.VJUST_CENTER:
                tpad = vdiff // 2
                bpad = vdiff - tpad
                new_content = [" " * component.get_width()] * tpad + \
                        new_content + \
                        [" " * component.get_width()] * bpad
            
            #stitch lines together
            for line in range(self.get_height()):
                to_render[line] += new_content[line]

        return self.justify(to_render)

class AbstractGrid(VSplitDisplay):
    """
    Text Display element that maintains a grid layout (which you will find 
    useful often...). Named after Ashleigh's ever faithful Canvas wiget that was
    sunset along with the GUI third of the course, paving the way for this
    monstrosity. Requires a fixed width and height to function (but does not 
    need to be square). 
    
    If the specified width or height is not equally
    divisible by the grid size, then the division rounds down, and the grid is 
    centered in the allocated space. Instead of the usual justification options,
    specify if (in the event of a rectangular width + height) you want the grid
    cells to be square based on the shorter measurement (square) or stretch to
    be rectangular (stretch). Cells are all BaseDisplay elements set to center 
    content.

    Can be indexed directly [row][column] to access the cells, 
    equivilantly use the get_cell method.

    NOTE: Resizing the grid, or changing the number of rows/collumns will wipe
    all content as the grid is reconstructed. 
    """

    # Alternate justification constants.
    GRID_SQUARE = "square"
    GRID_STRETCH = "stretch"
    
    _FIXED_GEO_ERR = DisplayError("Grid must have fixed geometry")

    def __init__(self, 
                 dims: tuple[int, int], #row col
                 width: int, 
                 height: int, 
                 just: str = GRID_SQUARE
    ):
        """
        Initialise a new AbstractGrid component.

        Args:
            dims (tuple[int, int]): dimensions of grid (rows, columns)
            width (int): fixed width.
            height (int): fixed height.
            just (str, optional): How grid should behave if width and height 
                                  are not equal. Can be either "square" or 
                                  "stretch". Defaults to "square".
        """
        if not width and height:
            raise self._FIXED_GEO_ERR
        
        super().__init__([], width, height)
        
        if just not in (self.GRID_SQUARE, self.GRID_STRETCH):
            raise DisplayError("invalid grid justification, please use "+ 
                             f"'{self.GRID_SQUARE}', or" +
                             f"'{self.GRID_STRETCH}'"
            )
        self._grid_just = just
        self.set_dims(dims)

    def set_width(self, width: int): # warning: wipes
        if not width:
            raise self._FIXED_GEO_ERR
        super().set_width(width)
        self.set_dims(self._dims) # Reconstruct grid with new geometry
    
    def set_height(self, height: int):
        if not height:
            raise self._FIXED_GEO_ERR
        super().set_height(height)
        self.set_dims(self._dims) # Reconstruct grid with new geometry

    def get_dims(self) -> tuple[int, int]: # warning: wipes
        """
        Return grid dimensions.

        Returns:
            tuple[int, int]: (row, column) dimensions.
        """
        return self._dims

    def set_dims(self, dims: tuple[int, int]): #Warning, wipes content
        """
        Set dimensions and reconstruct grid using them (wiping content)

        Args:
            dims (tuple[int, int]): new grid dimensions (rows, columns)
        """
        self._dims = dims

        # Determine cell dims
        cell_height = self._fixheight // dims[0]
        cell_width = self._fixwidth // dims[1]

        self.components().clear()
        for _ in range(dims[0]):
            if self._grid_just == self.GRID_SQUARE:
                min_dim = min(cell_height, cell_width)
                cell_height = min_dim
                cell_width = min_dim

            row_components = [BaseDisplay(width=cell_width, height=cell_height) 
                              for _ in range(dims[1])]
            self.components().append(HSplitDisplay(row_components, 
                                                   width=self.get_width(), 
                                                   height = cell_height)
            )

    def get_cell(self, row: int, col: int) -> BaseDisplay:
        """
        Return the BaseDisplay cell at the given coordinate.

        Args:
            row (int): row index
            col (int): column index

        Returns:
            BaseDisplay: BaseDisplay element at cell.
        """
        return self[row][col]
# ------------------------------------------------------------------------------


# Hearthstone specific view components
DISPLAY_WIDTH = 80

MINION_DISPLAY = "\U000023F8"
WYRM_DISPLAY = "\U00010426"
RAPTOR_DISPLAY = "\U00000D9E"

SHIELD_DISPLAY = "\U0001F6E1"

class CardDisplay(VSplitDisplay):
    """
    Displays a card with a border.
    """
    CARD_WIDTH = 12
    CARD_HEIGHT = 11
    CARD_HBORDER = ["+" + ("-" * CARD_WIDTH) + "+"]
    CARD_VBORDER = ["|"] * CARD_HEIGHT

    def __init__(self, padding: int) -> None:
        """
        Initializes the bordered card layout.

        Parameters:
            padding (int): Extra horizontal padding added to sides of card
                            for layout alignment.
        """
        super().__init__([
            BaseDisplay(
                [], 
                width = self.CARD_WIDTH + 2,
                height = 1    
            ),
            BaseDisplay(
                self.CARD_HBORDER, 
                width = self.CARD_WIDTH + 2,
                height = 1    
            ),
            HSplitDisplay([
                BaseDisplay(
                    self.CARD_VBORDER, 
                    width = 1,
                    height = self.CARD_HEIGHT   
                ),
                BaseDisplay(
                    width = self.CARD_WIDTH, 
                    height=self.CARD_HEIGHT,
                    vjust= CardDisplay.VJUST_TOP
                ),
                BaseDisplay(
                    self.CARD_VBORDER, 
                    width = 1,
                    height = self.CARD_HEIGHT   
                )  
            ]),
            BaseDisplay(
                self.CARD_HBORDER, 
                width = self.CARD_WIDTH + 2,
                height = 1    
            )
        ], 
        width = self.CARD_WIDTH + 2 + padding, 
        height = self.CARD_HEIGHT + 3
        )
        
    def set_card(self, card: "Card", num: int):
        """
        Populates the card display with content from a given Card object.

        Parameters:
            card (Card): The card object to render.
            num (int): The numeric identifier for the card.
        """
        # Adjust displayed number
        self[0].set_content([str(num),])

        # split name and desc
        text = str(card)
        split = text.split(": ")
        if len(split)> 1:
            name = split[0]
            desc = ": ".join(split[1:])
        else: #fallback in case students throw custom stuff in
            name = ""
            desc = text
        
        content = [name, f"Cost: {card.get_cost()}",""] # Insert cost stats
        content.extend(self[2][1].wrap_text(desc))
        
        self[2][1].set_content(content)

class HandDisplay(HSplitDisplay):
    """
        A horizontal layout for displaying a player's hand of cards.
    """
    V_BUFFER = 5
    def __init__(self, width: int = None) -> None:
        """
        Initializes an empty hand display area.

        Parameters:
            width (int, optional): Total width of the hand display.
        """
        super().__init__(
            [], width=width, height = CardDisplay.CARD_HEIGHT + self.V_BUFFER
        )
    
    def set_hand(self, hand: list["Card"]) -> None:
        """
        Populates the hand display with a list of card objects.

        Parameters:
            hand (list[Card]): The list of cards to be displayed.
        """
        self.components().clear()
        if hand:
            padding = (self.get_width() -
                   ((CardDisplay.CARD_WIDTH+2) * len(hand))) // len(hand)
        else: 
            padding = 0

        for i, card in enumerate(hand):
            card_display = CardDisplay(padding)
            card_display.set_card(card, i+1)
            self.components().append(card_display)



class MinionDisplay(AbstractGrid):
    """
    View class to display active minions
    """
    BOUNDARY_SEGMENT = "#"
    DIMS = (3,5)
    CELL_HEIGHT = 3

    DISPLAY_MAP = {
        MINION_SYMBOL: MINION_DISPLAY,
        RAPTOR_SYMBOL: RAPTOR_DISPLAY,
        WYRM_SYMBOL: WYRM_DISPLAY,
    }

    def __init__(self, width: int):
        """
        Initialise a new minion display

        Args:
            width (int): Width of display.
        """
        super().__init__(
            self.DIMS, 
            width, 
            self.DIMS[0]*self.CELL_HEIGHT, 
            self.GRID_STRETCH
        )

    def set_minions(self, 
                        player_minions: list["Minion"], 
                        enemy_minions: list["Minion"]
    ):
        """
        Display the given minions. Ignores minions after the fifth.

        Args:
            player_minions (list[Minion]): Player placed minions
            enemy_minions (list[Minion]): Enemy placed minions
        """
        for i in range(MAX_MINIONS):
            # Top row
            if i < len(enemy_minions):  
                minion = enemy_minions[i]
                content = [
                        f"{str(minion.get_health())} HP",
                        f"{self.DISPLAY_MAP[minion.get_symbol()]}"
                ]
                if minion.get_shield() > 0:
                    content.append(
                        f"{SHIELD_DISPLAY} ({str(minion.get_shield())})"
                    )
                self[0][i].set_content(content)
            else:
                self[0][i].set_content([])
            self[0][i].set_vjust(BaseDisplay.VJUST_TOP) # Teehee
            
            # Middle Row
            self[1][i].set_content([
                f"{i+1}",
                self.BOUNDARY_SEGMENT * self[1][i].get_width(),
                f"{i+MAX_MINIONS+1}"
            ])

            # Bottom row
            if i < len(player_minions): 
                minion = player_minions[i]
                content = [
                        f"{self.DISPLAY_MAP[minion.get_symbol()]}",
                        f"{str(minion.get_health())} HP",    
                ]
                if minion.get_shield() > 0:
                    content = [
                        f"{SHIELD_DISPLAY} ({str(minion.get_shield())})"
                    ] + content
                self[2][i].set_content(content)
            else:
                self[2][i].set_content([])
            self[2][i].set_vjust(BaseDisplay.VJUST_BOTTOM) # Teehee Moreso

class HeroView(HSplitDisplay):
    """
    Display component to depict Hero information
    """
    HERO_HEIGHT = 3
    def __init__(self, name: str, width: int):
        """
        Iniialise a new HeroView with the given name.

        Args:
            name (str): Name/tag to describe hero.
            width (int): fixed width of component.
        """
        nametag = BaseDisplay([name], hjust= BaseDisplay.HJUST_LEFT)
        stats = BaseDisplay(
            [], 
            hjust= BaseDisplay.HJUST_RIGHT, 
            width= width - nametag.get_width()
        )
        super().__init__(
            [nametag, stats],
            width = width,
            height = self.HERO_HEIGHT,
            hjust = self.HJUST_LEFT
        )

    def set_hero(self, hero: "Hero"):
        self[1].set_content([
            f"HP: {hero.get_health()}, {SHIELD_DISPLAY}: " +\
                f"{hero.get_shield()}, " +\
                    f"Cards Remaining: {hero.get_deck().remaining_count()}, " +\
                        f"Energy: {hero.get_energy()}/{hero.get_max_energy()}"
        ])

class HearthView(VSplitDisplay):
    """
    Text based GUI for a game of Hearthstone using structured prints to update 
    display. 
    """
    DIVIDER = "-" * DISPLAY_WIDTH
    TITLE = "HearthStone"

    def __init__(self):
        """
        Initialise a new text View.
        """
        header = BaseDisplay(
            [
                self.DIVIDER,
                self.TITLE,
                self.DIVIDER
            ],
            width = DISPLAY_WIDTH
        )
        enemy = HeroView(
            f"My Opponent! ({ENEMY_SELECT}): >:(",
            DISPLAY_WIDTH
        )
        minions = MinionDisplay(DISPLAY_WIDTH)
        cards = HandDisplay(DISPLAY_WIDTH)
        player = HeroView(
            f"Me! ({PLAYER_SELECT}): >:3",
            DISPLAY_WIDTH
        )
        message_bar = BaseDisplay(
            [self.DIVIDER, self.DIVIDER], 
            width = DISPLAY_WIDTH
        )

        super().__init__(
            [header, enemy, minions, cards, player, message_bar],
            width = DISPLAY_WIDTH
        )

    def update(self, 
            player: "Hero", 
            enemy: "Hero",
            player_minions: list["Minion"],
            enemy_minions: list["Minion"],
            messages: list[str]
    ):
        """
        Update display with the given entities and display to the user with a 
        structured print.

        Args:
            player (Hero): Player controlled Hero.
            enemy (Hero): Computer controlled Hero
            player_minions (list[Minion]): Player's active minions.
            enemy_minions (list[Minion]): Computer's active minions.
            messages (list[str]): Messages to display to user.
        """
        self[1].set_hero(enemy)
        self[2].set_minions(player_minions, enemy_minions)
        self[3].set_hand(player.get_hand())
        self[4].set_hero(player)
        self[5].set_content([self.DIVIDER] + messages + [self.DIVIDER])

        self.display()