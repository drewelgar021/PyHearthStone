# DO NOT modify or add any import statements
from support import *
from display import HearthView

# Name: Drew
# Student Number: 49599736
# Favorite Building: The Royal Exchange
# -----------------------------------------------------------------------------

class Card():
    """
    Card is an abstract class from which all instantiated types of card inherit.
    This class provides default card behavior, which can be inherited or 
    overridden by specific types of cards.
    """

    def __init__(self, **kwargs) -> None:
        """Constructor of <Card>."""

        self._name = CARD_NAME
        self._description = CARD_DESC
        self._symbol = CARD_SYMBOL
        self._cost = 1
        self._effect = {}
        self._is_permanent = False

    def __str__(self) -> str:
        return f"{self._name}: {self._description}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"
    
    def get_symbol(self) -> str:
        """Returns the symbol representing this card."""

        return self._symbol
    
    def get_name(self) -> str:
        """Returns the name of this card."""

        return self._name
    
    def get_cost(self) -> int:
        """ Returns the cost of this card."""

        return self._cost
    
    def get_effect(self) -> dict[str, int]:
        """Returns this card's effect."""

        return self._effect
    
    def is_permanent(self) -> bool:
        """Returns if this card is permanent or not."""

        return self._is_permanent


class Shield(Card):
    """Shield is a card that applies 5 shield to a target entity."""

    def __init__(self) -> None:
        """Constructor of <Shield>"""
        super().__init__()
        self._name = SHIELD_NAME
        self._description = SHIELD_DESC
        self._symbol = SHIELD_SYMBOL
        self._cost = 1
        self._effect = {SHIELD: 5}
        self._is_permanent = False


class Heal(Card):
    """Heal is a card that applies 2 health to a target entity."""

    def __init__(self) -> None:
        super().__init__()
        self._name = HEAL_NAME
        self._description = HEAL_DESC
        self._symbol = HEAL_SYMBOL
        self._cost = 2
        self._effect = {HEALTH: 2}
        self._is_permanent = False


class Fireball(Card):
    """
    Fireball is a card that applies 3 damage to a target entity. Fireball cards 
    apply 1 point of additional damage for each turn they have spent in a hero’s
    hand.
    """

    def __init__(self, turns_in_hand: int) -> None:
        """
        Constructor of <Fireball>.

        Arguments:
        turns_in_hand -- the number of turns that the card has spent in a hero's
                         hand
        """
        super().__init__()
        self._name = FIREBALL_NAME
        self._description = FIREBALL_DESC
        self._turns_in_hand = turns_in_hand
        self._symbol = str(self._turns_in_hand)
        self._cost = 3
        self._effect = {DAMAGE: (self._turns_in_hand + 3)}
        self._is_permanent = False

    def __str__(self) -> str:
        _damage = self._effect[DAMAGE]
        return f"{super().__str__()} Currently dealing {_damage} damage."

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._turns_in_hand})"

    def increment_turn(self) -> None:
        """
        Increments <_turns_in_hand> attribute by 1 to register another turn
        spent in a hero's hand
        """

        self._turns_in_hand += 1
        self._symbol = str(self._turns_in_hand)
        self._effect[DAMAGE] = self._turns_in_hand + 3


class CardDeck():
    """
    Represents an ordered deck of cards. Cards are drawn from the top of a 
    deck, and added to the bottom.
    """
    def __init__(self, cards: list[Card]) -> None:
        """Constructor for <CardDeck>."""

        self._cards = cards

    def __str__(self) -> str:
        _card_symbols = []
        for _card in self._cards:
            _card_symbols.append(_card.get_symbol())

        return ",".join(_card_symbols)

    def __repr__(self) -> str:
        return f"CardDeck({self._cards})"
    
    def is_empty(self) -> bool:
        """
        Returns <True> if this card deck is empty, returns <False> otherwise.
        """
        
        if len(self._cards) == 0:
            return True
        else:
            return False

    def remaining_count(self) -> int:
        """Returns how many cards are currently in this deck."""

        return len(self._cards)

    def draw_cards(self, num: int) -> list[Card]:
        """
        Draws the specified number of cards from the top of the deck. Cards 
        are returned in the order they are drawn. If there are not enough cards
        remaining in the deck, all cards in the deck are drawn.

        Arguments:
        num -- the number of cards to be drawn from the top of the deck
        """

        if num > len(self._cards): # not enough cards so draw all
            _cards_to_draw = self._cards.copy()
            self._cards = []
            return _cards_to_draw
        else:
            _cards_to_draw = self._cards[0:num]
            del self._cards[0:num]
            return _cards_to_draw

    def add_card(self, card: Card) -> None:
        """
        Adds the given card to the bottom of the deck
        
        Arguments:
        card -- the card to be added
        """

        self._cards.append(card)


class Entity():
    """
    Entity is an abstract class from which all instantiated types of entity 
    inherit. This class provides default entity behavior, which can be 
    inherited or overridden by specific types of entities. Each entity has a
    health and shield value, and are alive if and only if their health value
    is above 0.
    """

    def __init__(self, health: int, shield: int) -> None:
        """
        Constructor for <Entity>.

        Arguments:
        health -- starting health value for the new entity.
        shield -- starting shield value for the new entity.
        """

        self._health = health
        self._shield = shield
        
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._health}, {self._shield})"
    
    def __str__(self) -> str:
        return f"{self._health},{self._shield}"
    
    def get_health(self) -> int:
        """Returns this entity's health."""

        return self._health

    def get_shield(self) -> int:
        """Returns this entity's shield."""

        return self._shield
    
    def apply_shield(self, shield: int) -> None:
        """
        Applies the given amount of shield.

        Arguments:
        shield -- the amount of shield to be added to the entity.
        """

        self._shield += shield

    def apply_health(self, health) -> None:
        """
        Applies the given number of health points to the entity.

        Arguments:
        health -- the amount of health to be added to the entity.
        """

        self._health += health

    def apply_damage(self, damage: int) -> None:
        """
        Applies the given amount of damage.  Does not allow the entity's health 
        to drop below 0.  any damage exceeding the amount required to reduce the
        entity's health to 0 is discarded.

        Arguments:
        damage -- the amount of damage to be applied to the entity.
        """

        if damage <= self._shield:
            self._shield -= damage
        else:
            _damage_to_health = damage - self._shield
            self._shield = 0
            self._health -= _damage_to_health
            if self._health < 0:
                self._health = 0 # reset health to 0 if it goes negative
            
    def is_alive(self) -> bool:
        """Returns <True> if this entity is alive, or <False> otherwise."""

        return self._health > 0


class Hero(Entity):
    """
    A Hero is an entity with the agency to take actions in the game, possessing 
    an energy level (and corresponding energy capacity), a deck of cards, and a 
    hand of cards. When a hero is instantiated, its energy level is always at 
    maximum capacity. A hero’s maximum hand size is 5. Unlike a base entity, a 
    hero is only alive when both its health and the number of cards in its deck 
    are greater than 0.
    """

    def __init__(
            self, health: int, shield: int, max_energy: int,
            deck: CardDeck, hand: list[Card]
        ) -> None:
        """
        Constructor for <Hero>

        Arguments:
        health -- starting health value for the new entity.
        shield -- starting shield value for the new entity.
        max_energy -- the hero's maximum energy capacity.
        deck -- CardDeck belonging to the hero.
        hand -- list of cards that make up the hero's hand.
        """
        
        super().__init__(health, shield)
        self._energy_capacity = self._energy = max_energy
        self._deck = deck
        self._hand = hand
    
    def __str__(self) -> str:
        _stats = f"{self._health},{self._shield},{self._energy_capacity}"
        _hand_symbols = ",".join([card.get_symbol() for card in self._hand])

        return f"{_stats};{str(self._deck)};{str(_hand_symbols)}"
    
    def __repr__(self) -> str:
        _stats = f"{self._health}, {self._shield}, {self._energy_capacity}"
        return f"Hero({_stats}, {repr(self._deck)}, {self._hand})"

    def get_energy(self) -> int:
        """Returns the hero's current energy level."""

        return self._energy
    
    def spend_energy(self, energy: int) -> bool:
        """
        Attempts to spend the specified amount of this hero’s energy. If this 
        hero does not have sufficient energy, then nothing happens. Returns 
        <True> if the energy was spent, or <False> otherwise.

        Arguments:
        energy -- amount of energy to be spent.
        """

        if energy <= self._energy:
            self._energy -= energy
            return True
        else:
            return False

    def get_max_energy(self) -> int:
        """Returns this hero's energy capacity."""

        return self._energy_capacity
    
    def get_deck(self) -> CardDeck:
        """Returns this hero's deck."""
        
        return self._deck
    
    def get_hand(self) -> list[Card]:
        """Returns this hero's hand in order, as a list."""

        return self._hand
    
    def new_turn(self) -> None:
        """
        Registers a new turn of all fireball cards in this hero’s hand, draws 
        from their deck into their hand, expands their energy capacity by 1, 
        and refills their energy level.
        """

        for card in self._hand:  # increment turn of all fireball cards
            if card.get_name() == FIREBALL_NAME:
                card.increment_turn()
        
        _num_to_draw = 5 - len(self._hand)  # calculate number of cards to draw
                                            # such that hero has max 5 cards
        self._hand += self._deck.draw_cards(_num_to_draw)

        self._energy_capacity += 1
        self._energy = self._energy_capacity

    def is_alive(self):
        """Returns <True> if this hero is alive, or <False> otherwise."""

        # superclass method checks if health > 0, hero must also have number
        # of cards in deck > 0 to be alive
        return super().is_alive() and self._deck.remaining_count() > 0


class Minion(Card, Entity):
    """
    Minion is an abstract class from which all instantiated types of minion 
    inherit. This class provides default minion behavior, which can be inherited
    or overridden by specific types of minions. Minions are a special type of 
    Card that also inherits from Entity. Its __init__ method takes in the 
    arguments of the Entity class. All minions are permanent cards. Generic 
    Minions have cost 2, no effect, and are represented by the symbol M.

    A minion has the capacity to select its own target entity out of a given 
    set. Generic minions ignore all given entities, and returns itself.
    """

    def __init__(self, health: int, shield: int) -> None:
        """
        Constructor for <Minion>.

        Arguments:
        health -- starting health value for the new entity.
        shield -- starting shield value for the new entity.
        """

        Card.__init__(self)
        Entity.__init__(self, health, shield)
        
        self._name = MINION_NAME
        self._symbol = MINION_SYMBOL
        self._cost = 2
        self._is_permanent = True

    def __str__(self) -> str:
        return f"{MINION_NAME}: {MINION_DESC}"
    
    def __repr__(self):
        return Entity.__repr__(self)

    def choose_target(
            self, ally_hero: Entity, enemy_hero: Entity,
            ally_minions: list[Entity], enemy_minions: list[Entity]
        ) -> Entity:
        """
        Select this minion’s target out of the given entities. Note that 
        here, the allied hero and minions will be those friendly to this minion,
        not necessarily to the player. This logic extends to the specified enemy
        hero and minions. Minions should be provided in the order they appear in
        their respective minion slots, from left to right.

        Arguments:
        ally_hero -- the hero to be targeted by healing effects 
                     (health and shield)
        enemy_hero -- the hero to be targeted by attacks
        ally_minions -- the list of minions to be targeted by healing effects
                        (health and shield)
        enemy_minions -- the list of minions to be targeted by attacks
        """
        
        return self


class Wyrm(Minion):
    """
    A Wyrm is a minion that has 2 cost, is represented by the symbol W, and 
    whose effect is to apply 1 heal and 1 shield.
    """

    def __init__(self, health, shield) -> None:
        """
        Constructor for <Wyrm>.

        Arguments:
        health -- starting health value for the new entity.
        shield -- starting shield value for the new entity.
        """
        
        super().__init__(health, shield)
        self._name = WYRM_NAME
        self._symbol = WYRM_SYMBOL
        self._effect = {HEALTH: 1, SHIELD: 1}

    def __str__(self) -> str:
        return f"{WYRM_NAME}: {WYRM_DESC}"

    def choose_target(
            self, ally_hero: Entity, enemy_hero: Entity,
            ally_minions: list[Entity], enemy_minions: list[Entity]
        ) -> Entity:
        """
        When selecting a target entity, a Wyrm will choose the allied entity
        with the lowest health. If multiple entities have the lowest health, if
        one of the tied entities is the allied hero, the <ally_hero> is
        selected. Otherwise, the leftmost minion is selected.

        Arguments:
        ally_hero -- the hero to be targeted by healing effects (health and
                     shield).
        enemy_hero -- the hero to be targeted by attacks.
        ally_minions -- the list of minions to be targeted by healing effects
                        (health and shield).
        enemy_minions -- the list of minions to be targeted by attacks.
        """

        _lowest_health = ally_hero  # default is hero so that all minions'
                                    # health must be strictly lower than hero's
                                    # for them to be selected as target
        for minion in ally_minions:
            if minion.get_health() < _lowest_health.get_health():
                # leftmost minion is selected in tie since strict < is used
                _lowest_health = minion

        return _lowest_health


class Raptor(Minion):
    """
    A Raptor is a minion that has 2 cost, is represented by the symbol R, and 
    whose effect is to apply damage equal to its health.
    """

    def __init__(self, health, shield) -> str:
        """
        Constructor for <Raptor>.

        Arguments:
        health -- starting health value for the new entity.
        shield -- starting shield value for the new entity.
        """

        super().__init__(health, shield)
        self._name = RAPTOR_NAME
        self._symbol = RAPTOR_SYMBOL
        self._effect = {DAMAGE: self._health}

    def __str__(self) -> str:
        return f"{RAPTOR_NAME}: {RAPTOR_DESC}"
    
    def get_effect(self):
        self._effect[DAMAGE] = self._health
        return self._effect

    def choose_target(
            self, ally_hero: Entity, enemy_hero: Entity,
            ally_minions: list[Entity], enemy_minions: list[Entity]
        ) -> Entity:
        """
        When selecting a target entity, a Raptor will choose the enemy minion 
        with the highest health. If there is no such minion. If multiple minions
        have the highest health, the leftmost minion is selected. If there are
        no enemy minions, the <enemy_hero> is selected

        Arguments:
        ally_hero -- the hero to be targeted by healing effects 
                     (health and shield)
        enemy_hero -- the hero to be targeted by attacks
        ally_minions -- the list of minions to be targeted by healing effects
                        (health and shield)
        enemy_minions -- the list of minions to be targeted by attacks
        """
        
        if len(enemy_minions) > 0:
            _highest_health = enemy_minions[0]
            for minion in enemy_minions:
                if minion.get_health() > _highest_health.get_health():
                    # leftmost minion is selected in tie since strict > is used
                    _highest_health = minion

            return _highest_health
        
        else:  # target hero if there are no minions
            return enemy_hero

class HearthModel():
    """
    Here, active minions are those minions currently existing within a minion 
    slot. Both the player and their opponent have a maximum of 5 minion slots. 
    Minion slots are filled out from left to right. If a minion is to be placed 
    and all respective minion slots are full, the minion in the leftmost minion 
    slot is removed from the game, and all minions in remaining slots are moved 
    one slot left before the new minion is placed.

    Within this model, the enemy hero follows the following logic: When the 
    enemy hero takes a turn, it attempts to play each card in its hand in order.
    Whenever it successfully plays a card, it begins trying cards from the 
    beginning of its hand again. If the enemy plays a card that includes a 
    damage effect, it always targets the player’s hero. Otherwise it targets 
    itself.
    """

    def __init__(
            self, player: Hero, active_player_minions: list[Minion],
            enemy: Hero, active_enemy_minions: list[Minion]
        ) -> None:
        """
        Constructor for <HearthModel>.

        Arguments:
        player -- the Hero to be controlled by the player
        active_player_minions -- list of the player's minions active in minion
                                 slots
        enemy: the Hero to be played against by the player
        active_enemy_minions -- list of the enemy's minions active in minion
                                slots

        """
        self._player = player
        self._active_player_minions = active_player_minions
        self._enemy = enemy
        self._active_enemy_minions = active_enemy_minions

    def _get_minion_info(self, minions: list[Minion]) -> str:
        _info_list = []

        for _minion in minions:
            _minion_info = (
                f"{_minion.get_symbol()},"
                f"{_minion.get_health()},"
                f"{_minion.get_shield()}"
            )
            
            _info_list.append(_minion_info)

        return ";".join(_info_list)
                

    def __str__(self) -> str:
        return (
            f"{str(self._player)}|"
            f"{self._get_minion_info(self._active_player_minions)}|"
            f"{str(self._enemy)}|"
            f"{self._get_minion_info(self._active_enemy_minions)}"
        )
    
    def __repr__(self) -> str:
        return (
            "HearthModel("
                f"{repr(self._player)}, {self._active_player_minions}, "
                f"{repr(self._enemy)}, {self._active_enemy_minions}"
            ")"
        )
    
    def get_player(self) -> Hero:
        """Return this model's player hero instance."""

        return self._player
    
    def get_enemy(self) -> Hero:
        """Return this model's enemy hero instance."""

        return self._enemy
    
    def get_player_minions(self) -> list[Minion]:
        """
        Return the player’s active minions. Minions should appear in order 
        from leftmost minion slot to rightmost minion slot.
        """

        return self._active_player_minions
    
    def get_enemy_minions(self) -> list[Minion]:
        """
        Return the enemy’s active minions. Minions should appear in order from 
        leftmost minion slot to rightmost minion slot.
        """

        return self._active_enemy_minions
    
    def has_won(self) -> bool:
        """
        Return true if and only if the player has won the game.
        
        The player wins when their hero is not defeated, and their opponents'
        hero is defeated.
        """

        return self._player.is_alive() and not self._enemy.is_alive()
    
    def has_lost(self) -> bool:
        """
        Return true if and only if the player has lost the game.

        The player loses when their hero is defeated.
        """

        return not self._player.is_alive()

    def _remove_defeated_minions(self) -> None:
        # create lists of only alive minions and replace active minion lists
        _alive_player_minions = [
            _minion
            for _minion in self._active_player_minions
            if _minion.is_alive() 
        ]
        self._active_player_minions = _alive_player_minions.copy()
        
        _alive_enemy_minions = [
            _minion
            for _minion in self._active_enemy_minions
            if _minion.is_alive()
        ]
        self._active_enemy_minions = _alive_enemy_minions.copy()
        

    def _use_effect(self, card: Card, target: Entity) -> None:
        # remove defeated minions before effect is used to prevent minion with
        # 0 health being healed
        self._remove_defeated_minions()
        if DAMAGE in card.get_effect():
            target.apply_damage(card.get_effect()[DAMAGE])

        if HEALTH in card.get_effect():
            target.apply_health(card.get_effect()[HEALTH])

        if SHIELD in card.get_effect():
            target.apply_shield(card.get_effect()[SHIELD])
        # remove defeated minions after effect is used in case one's health
        # has been reduced to 0
        self._remove_defeated_minions()

    def play_card(self, card: Card, target: Entity) -> bool:
        """
        Attempts to play the specified card on the player's behalf. Returns 
        whether the card was successfully played or not. The target argument 
        will be ignored if the specified card is permanent.

        Arguments:
        card -- the card to be played from the player's hand
        target -- entity affected by the card (if it is not permanent)
        """

        if self._player.spend_energy(card.get_cost()):

            self._player.get_hand().remove(card)

            if card.is_permanent():
                if len(self._active_player_minions) == 5:
                    # restrict to max 5 minions
                    self._active_player_minions.pop(0)
                self._active_player_minions.append(card)
                
                while len(self._active_player_minions) > 5:
                    self._active_player_minions.pop[0]  # keep max of 5 minions

            else:
                # use effect straight away if card is not permenant
                self._use_effect(card, target)

            return True # card was played
        
        else:
            return False # card was not played
        
    def discard_card(self, card: Card):
        """
        Discards the given card from the player's hand. This card is added to
        the bottom of the player's deck.

        Arguments:
        card -- the card to be discarded from the player's hand
        """

        self._player.get_deck().add_card(card)
        self._player.get_hand().remove(card)

    def end_turn(self) -> list[str]:
        """
        Ends the current turn.

        Returns the names of the cards played by the enemy hero (in order).
        """

        for _minion in self._active_player_minions:
            _target = _minion.choose_target(
                self._player, self._enemy,
                self._active_player_minions, self._active_enemy_minions
            )
            self._use_effect(_minion, _target)

        self._enemy.new_turn()

        if not self._enemy.is_alive():
            return [] # as the enemy did not play any cards

        _played_cards = []
        _playing_cards = True
        while _playing_cards:
            _skipped_cards = 0
            
            for _card in self._enemy.get_hand():
                if self._enemy.spend_energy(_card.get_cost()):
                    if _card.is_permanent():
                        # restrict to max 5 minions
                        if len(self._active_enemy_minions) == 5:
                            self._active_enemy_minions.pop(0)

                        self._active_enemy_minions.append(_card)

                    else:
                        if DAMAGE in _card.get_effect():
                            # target player if card includes damage effect
                            self._use_effect(_card, self._player)

                        else:
                            # otherwise enemy targets self
                            self._use_effect(_card, self._enemy)

                    _played_cards.append(type(_card).__name__)
                    self._enemy.get_hand().remove(_card)

                    break  # return to start of hand if a card is played
                else:
                    _skipped_cards += 1

            if _skipped_cards >= len(self._enemy.get_hand()):
                # stop playing cards once enemy tries every card in hand without
                # successfully playing one
                _playing_cards = False

        # all enemy minions use their effects on their chosen target
        for _minion in self._active_enemy_minions:
            _target = _minion.choose_target(
                self._enemy, self._player,
                self._active_enemy_minions, self._active_player_minions
            )
            self._use_effect(_minion, _target)
            

        self._player.new_turn()
    
        return _played_cards

class Hearthstone():
    """
    Hearthstone() is the controller class for the overall game. The controller
    is responsible for creating and maintaining instances of the model and view
    classes, handling player input, and facilitating communication between the
    model and view classes.
    """

    def __init__(self, file: str) -> None:
        """
        Instantiates the controller. Creates view and model instances. The model
        is instantiated with the game state specified by the data within the
        <file>.

        Arguments:
        file -- the save file containing the game state to load.
        """

        self.load_game(file)
        self._view = HearthView()

    def __str__(self) -> str:
        return f"{CONTROLLER_DESC}{self._file_name}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._file_name})"

    def update_display(self, messages: list[str]) -> None:
        """
        Update the display by printing out the current game state.
        
        Arguments:
        messages -- list of messages to be displayed at the bottom of the game
                    screen
        """

        self._view.update(
            self._model.get_player(),
            self._model.get_enemy(),
            self._model.get_player_minions(),
            self._model.get_enemy_minions(),
            messages
        )

    def get_command(self) -> str:
        """
        Repeatedly prompts the user until they enter a valid command. Returns
        the first valid command entered by the user. The player’s command will
        be case insensitive, but the returned command should be lower case. Note
        also that card positions will be entered one-indexed.
        """

        while True:
            _command = input(COMMAND_PROMPT).lower()

            if (
                _command in [HELP_COMMAND, END_TURN_COMMAND]
                or (
                    len(_command.split()) == 2
                    and (
                        _command.split()[0] == LOAD_COMMAND
                        or

                        _command.split()[0] in [PLAY_COMMAND, DISCARD_COMMAND]
                        and
                        _command.split()[1].isdigit()
                        and
                        int(_command.split()[1]) in range(
                            #  check that index maps to existing card in hand
                            1, len(self._model.get_player().get_hand()) + 1
                        )
                    )
                )
            ):
                return _command

            else:
                self.update_display([INVALID_COMMAND])

    def get_target_entity(self) -> str:
        """
        Repeatedly prompts the user until they enter a valid entity identifier.
        A valid entity identifier is one of the following: PLAYER_SELECT or
        ENEMY_SELECT from support.py, to select the player or enemy hero
        respectively; an integer between 1 and 5 inclusive, to select the minion
        in the enemy’s minion slot at the respective position; or an integer
        between 6 and 10 inclusive, to select the minion in the player’s minion
        slot at the position given by the subtracting 5 from the integer.

        If a hero is selected, the identifier is returned directly. If an
        enemy’s minion is selected, the (zero-indexed) index of the minion in
        the enemy’s minion slots is returned prepended by ENEMY_SELECT from
        support.py. If an player’s minion is selected, the (zero-indexed) index
        of the minion in the player’s minion slots is returned prepended by
        PLAYER_SELECT from support.py.
        """

        while True:
            _target = input(ENTITY_PROMPT).upper()
            if _target in [PLAYER_SELECT, ENEMY_SELECT]:
                return _target
            elif (
                _target.isdigit()
                and
                int(_target) in range(1, 6)
                and  #  checks if there is a minion in given slot
                len(self._model.get_enemy_minions()) >= int(_target)
            ):
                return f"{ENEMY_SELECT}{int(_target) - 1}"
            
            elif (
                _target.isdigit()
                and
                int(_target) in range(6, 11)
                and
                len(self._model.get_player_minions()) >= int(_target) - 5
            ):
                return f"{PLAYER_SELECT}{int(_target) - 6}"
            
            else:
                self.update_display([INVALID_ENTITY])

    def save_game(self) -> None:
        """
        Writes the string representation of this controllers HearthModel
        instance to autosave.txt. If autosave.txt does not exist, it is created.
        If autosave.txt already has content in it, it is overwritten. A game
        state can be loaded from this file using Hearthstone.load_game
        """

        with open(SAVE_LOC, "w") as _autosave:
            _autosave.write(str(self._model))

    def _generate_cards(self, cards: str) -> list[Card]:
        _card_list = []
        for _symbol in cards.split(","):
            if _symbol == CARD_SYMBOL:
                _card_list.append(Card())

            elif _symbol == SHIELD_SYMBOL:
                _card_list.append(Shield())
            
            elif _symbol == HEAL_SYMBOL:
                _card_list.append(Heal())
            
            elif _symbol.isdigit():
                _card_list.append(Fireball(int(_symbol)))
            
            elif _symbol == MINION_SYMBOL:
                _card_list.append(Minion(1, 0))
            
            elif _symbol == RAPTOR_SYMBOL:
                _card_list.append(Raptor(1, 0))
            
            elif _symbol == WYRM_SYMBOL:
                _card_list.append(Wyrm(1, 0))
        
        return _card_list

    def _generate_hero(self, hero: str) -> Hero:
        _stats, _deck_symbols, _hand_symbols = hero.split(";")

        _health, _shield, _max_energy = _stats.split(",")
        
        _deck = CardDeck(self._generate_cards(_deck_symbols))
        _hand = self._generate_cards(_hand_symbols)

        return Hero(int(_health), int(_shield), int(_max_energy), _deck, _hand)
    
    def _generate_minions(self, minions: str) -> list[Minion]:
        _minion_list = []
        if minions.strip() != "":
            for _minion in minions.split(";"):
                _symbol, _health, _shield = _minion.split(",")
                if _symbol == MINION_SYMBOL:
                    _minion_list.append(Minion(int(_health), int(_shield)))
                
                elif _symbol == RAPTOR_SYMBOL:
                    _minion_list.append(Raptor(int(_health), int(_shield)))
                
                elif _symbol == WYRM_SYMBOL:
                    _minion_list.append(Wyrm(int(_health), int(_shield)))

        return _minion_list

    def load_game(self, file: str) -> None:
        """
        Replaces the current model instance with a new one loaded from the data
        within <file>, taking the form of a string represented <HearthModel>.
        
        Minions that are not currently in a minion slot are instantiated with 1
        health and 0 shield. Does not handle the case where the file with the
        specified name does not exist, nor does it handle the case where the
        file does not contain a valid game state.

        When loading a game state from a file, it is expected that the first
        line of the file contains the string representation of a <HearthModel>
        instance. Any content after the first line of a file is ignored when
        loading a game state from it.

        Arguments:
        file -- the save file containing the game state to load.
        """

        self._file_name = file

        with open(file, "r") as _file:
            # read game state from first line of file
            _game_state = _file.readline()

        _game_data = _game_state.split("|")

        _player = _game_data[0]
        _active_player_minions = _game_data[1]
        _enemy = _game_data[2]
        _active_enemy_minions = _game_data[3]

        self._model = HearthModel(
            self._generate_hero(_player),
            self._generate_minions(_active_player_minions),
            self._generate_hero(_enemy),
            self._generate_minions(_active_enemy_minions)
        )

    def play(self):
        """Conducts a game of Hearthstone from start to finish."""

        _model = self._model
        self.update_display([WELCOME_MESSAGE])

        while not (_model.has_won() or _model.has_lost()):
            _command = self.get_command()
            
            if _command == HELP_COMMAND:
                _messages = HELP_MESSAGES

            elif _command.split()[0] == PLAY_COMMAND:
                _card_index = int(_command.split()[1]) - 1
                _card = _model.get_player().get_hand()[_card_index]

                if _card.is_permanent():
                    _target = True  # dummy target to be ignored

                else:
                    _target_input = self.get_target_entity()

                    if _target_input == PLAYER_SELECT:
                        _target = _model.get_player()
                    elif _target_input == ENEMY_SELECT:
                        _target = _model.get_enemy()
                    
                    elif len(_target_input) > 1:  # target is a minion
                        _minion_index = int(_target_input[1])
                        
                        if _target_input[0] == PLAYER_SELECT:
                            _target = _model.get_player_minions()[_minion_index]
                        
                        elif _target_input[0] == ENEMY_SELECT:
                            _target = _model.get_enemy_minions()[_minion_index]

                if _model.play_card(_card, _target):
                    _messages = [f"{PLAY_MESSAGE}{type(_card).__name__}"]
                else:
                    _messages = [ENERGY_MESSAGE]

            elif _command.split()[0] == DISCARD_COMMAND:
                _card_index = int(_command.split()[1]) - 1
                _card = _model.get_player().get_hand()[_card_index]
                _model.discard_card(_card)
                
                _messages = [f"{DISCARD_MESSAGE}{type(_card).__name__}"]

            elif _command.split()[0] == LOAD_COMMAND:
                _file_name = _command.split()[1]
                try:
                    self.load_game(_file_name)
                    # need to update _model as it will otherwise store the old
                    # self._model
                    _model = self._model
                    _messages = [f"{GAME_LOAD_MESSAGE}{_file_name}"]
                except FileNotFoundError:
                    _messages = [f"{_file_name}{NO_FILE_MESSAGE}"]
                except Exception as _exception:
                    _messages = [f"{BAD_FILE_MESSAGE}{str(_exception)}"]

            elif _command == END_TURN_COMMAND:
                _messages = []
                for _card in _model.end_turn():
                    _messages.append(f"{ENEMY_PLAY_MESSAGE}{_card}")

                if not (_model.has_won() or _model.has_lost()):
                    self.save_game()
                    _messages.append(GAME_SAVE_MESSAGE)

            if _model.has_won():
                _messages.append(WIN_MESSAGE)
            if _model.has_lost():
                _messages.append(LOSS_MESSAGE)
                
            self.update_display(_messages)


def play_game(file: str) -> None:
    """
    Constructs a HearthModel instance with the game state within <file> to enact
    a single game of Hearthstone from beginning to end. If an exception is raied
    when attempting to load <file> the default save file at <SAVE_LOC> will be
    loaded instead.

    Arguments:
    file -- the game state to load.
    """

    try:
        hs = Hearthstone(file)
    except Exception:
        hs = Hearthstone(SAVE_LOC)
    
    hs.play()






def main() -> None:
    """Executes <play_game> using the default save location."""
    play_game(SAVE_LOC)

if __name__ == "__main__":
    main()