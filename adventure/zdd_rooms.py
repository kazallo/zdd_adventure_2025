"""This is to keep all special rooms of the ZDD."""
from main_classes import Room


class ToiletCellar(Room):
    def run_story(self, user_items):
        print("What did you expect? It's a toilet.")
        # Check by name; if the book is present, drop it (story event)
        if "old book" in [x.name for x in user_items]:
            print("While you wash your hands, the book slips out of your backpack ...right into the water.")
            print("You decide that it wasn't that important after all.")
            # Remove book from inventory
            return [x for x in user_items if x.name != "old book"]
        return user_items

class Basement51(Room):
    """
    A hidden room with an audio-based password puzzle. Fully integrated into
    the normal room system: global commands work, the player can still leave,
    and the puzzle state is preserved.
    """

    def __init__(self, name, description, items_init=None):
        super().__init__(name, description, items_init)
        self.password = "2431"
        self.puzzle_solved = False

    def run_story(self, user_items):
        """Prints intro text only the first time the player enters."""
        if self.visited == 1:
            print("You push open a heavy iron door...")
            print("Old, rusted machines cover the room. Strange rhythmic beeping fills the air.")
            print("A dusty terminal sits in the corner. Next to it: a locked metal locker.")
            print("Above everything, a faded sign reads: ROOM 51.")
            print("Below the sign: a locker with a numerical lock.\n")
        return user_items

    def show_items(self, user_items):
        """Override: instead of listing items, we run the puzzle menu."""
        return self.puzzle_loop(user_items)

    def puzzle_loop(self, user_items):
        """
        The interactive part of the room. Runs when the player chooses 'inspect'.
        Global commands still work because command_handler handles them.
        """
        command_handler = self._get_command_handler()

        while True:
            print("\nYou can:")
            print("  • Inspect the machines   (inspect)")
            print("  • Listen to the sounds   (listen)")
            print("  • Try to open the locker (open)")
            print("  • Check the terminal     (terminal)")
            print("  • Leave the puzzle menu  (back)\n")

            action = input("▶ What do you do? ").strip().lower()

            # Allow global commands (inventory, help, exit)
            if command_handler.handle_global_commands(action):
                if not command_handler.game.game_active:
                    return user_items
                continue

            if action == "back":
                print("You step away from the machines.")
                return user_items

            elif action == "inspect":
                print("The machines are dusty and ancient. They don't seem operational.")

            elif action == "terminal":
                print("The terminal is dead. No power, no display.")

            elif action == "listen":
                self.play_text_beeps()

            elif action == "open":
                self.try_open_locker()

            else:
                print("That's not a valid action.")

    # ------------------------------------------------------------
    # Puzzle mechanics
    # ------------------------------------------------------------

    def play_text_beeps(self):
        """
        Prints the beep sequence visually instead of using winsound.
        Works on all systems.
        """
        print("\nYou close your eyes and listen carefully...")
        print("(Tip: Count the number of beeps in each group.)\n")

        for digit in self.password:
            n = int(digit)
            print("Beep " * n)
            print("---")
        print()

    def try_open_locker(self):
        if self.puzzle_solved:
            print("The locker is already open.")
            return

        attempt = input("▶ Enter password: ").strip()
        if attempt == self.password:
            print("\nThe lock clicks open!")
            print("Inside you find an old notebook with a faded message:")
            print("  04/12/2025 – Day 285")
            print("  Subject #341 escaped. Containment status: UNKNOWN.")
            print("  If you're reading this, shut down the system and save our world!")
            print("\nSomeone tried… but clearly failed.\n")
            self.puzzle_solved = True
        else:
            print("Incorrect password.")
            print("Maybe listening to the beeps will help...")

    # ------------------------------------------------------------
    # Helper to access the command handler (cleanly)
    # ------------------------------------------------------------
    def _get_command_handler(self):
        """
        Retrieves the command handler from the active adventure.
        Rooms normally don't store a reference, so this traverses
        back through the floors to find the game object.
        """
        # This trick uses the fact that Floor.rooms stores the same instance
        # and the game sets current_room before entering.
        import inspect

        for frame_info in inspect.stack():
            local_vars = frame_info.frame.f_locals
            if "self" in local_vars and hasattr(local_vars["self"], "command_handler"):
                return local_vars["self"].command_handler

        raise RuntimeError("CommandHandler not found from room context.")
# -----------------------------------------------------------
# ------------------- List here all rooms -------------------
toilet_cellar = ToiletCellar("toilet", "Yes, even the cellar has a toilet.")
Room_51 = Basement51("Room 51","A hidden Room with a heavy iron door.")
# -----------------------------------------------------------
# Add YOUR ROOM instance here, similar to the example below:
# my_room = MyRoom("room_name", "room_description")

ALL_ROOMS = {
    "toilet_cellar": toilet_cellar,
    "Room 51"      : Room_51
    # Add your room key-value pairs here:
    # "my_room_key": my_room
}
