from main_classes import CommandHandler, Item, Floor, Room, UI
from zdd_rooms import ALL_ROOMS

EXIT_COMMAND = "exit"


class ZDDAdventure:
    def __init__(self):
        self.items = []
        self.floors = self.create_floors()
        self.current_floor = self.floors["cellar"]
        self.current_room = None
        self.game_active = True
        self.command_handler = CommandHandler(self)

    def create_floors(self):
        # Define the floors
        cellar = Floor("cellar", "It's a bit chilly here. The only light is coming from the emergency lights.")
        ground_floor = Floor("ground floor", "You see a open working space with all kind of stuff standing around... weird.")
        first_floor = Floor("first floor", "There are many doors. Study rooms, offices, and labs.")
        second_floor = Floor("second floor", "This floor hosts the professors' offices and some research labs.")
        third_floor = Floor("third floor", "This is the topmost floor with the lecture hall and a meeting room. You have heard about a roof terrace, but that might just be stories...")
        # roof_floor = Floor("roof", "You really shouldn't be here!!!")

        # Connect floors
        cellar.add_connection("up", ground_floor)
        ground_floor.add_connection("down", cellar)
        ground_floor.add_connection("up", first_floor)
        first_floor.add_connection("down", ground_floor)
        first_floor.add_connection("up", second_floor)
        second_floor.add_connection("down", first_floor)
        second_floor.add_connection("up", third_floor)
        third_floor.add_connection("down", second_floor)

        # Define rooms in each floor
        analog_book = Item("old book", "a real book made of paper", movable=True)
        archive_room = Room("archive", "Old records and dusty books everywhere.", analog_book)
        cellar.add_room("archive", archive_room)
        cellar.add_room("toilet", ALL_ROOMS["toilet_cellar"])
        cellar.add_room("Room 51",ALL_ROOMS["Room 51"])
        # -------------------------------
        # ... Add other rooms ...

        return {
            "cellar": cellar,
            "ground floor": ground_floor,
            "first floor": first_floor,
            "second floor": second_floor,
            "third floor": third_floor,
        }

    def play(self):
        introduction = (
            "... slowly ... you .... wake ... up ...\n"
            "You are in a huge room with very little light...\n"
            "Wait! \nThat's the 'Data Science and AI lab' in the cellar of the ZDD!\n"
            "Adrenaline kicks in.\nYou look around.\nWhat is going on?\nWhere is everyone else?\n"
            "You quickly leave the room. But there's no one on the hallway either."
        )
        print(UI.title("ZDD TEXT ADVENTURE"))
        print(introduction)
        print(UI.divider())

        while self.game_active:
            # Floor header & orientation
            print(UI.title(self.current_floor.name.upper()))
            print(UI.panel("AREA", self.current_floor.description))
            print(self.current_floor.get_orientation())
            print(UI.hint("Type 'help' for commands or 'inventory' to check what you're carrying."))
            print(UI.divider())

            action = input("▶ What do you do? ").strip().lower()

            # 1) Global commands
            if self.command_handler.handle_global_commands(action):
                if not self.game_active:
                    break
                continue

            # 2) Navigation: change the floor
            if action.startswith("go "):
                parts = action.split(maxsplit=1)
                if len(parts) < 2 or not parts[1]:
                    print("Please specify a direction, e.g. 'go up'.")
                    continue
                direction = parts[1]
                next_floor = self.current_floor.get_floor_in_direction(direction)
                if next_floor:
                    self.current_floor = next_floor
                    self.current_room = None
                else:
                    print("You can't go in that direction!")
                continue

            # 3) Rooms: enter a room
            if action.startswith("enter "):
                parts = action.split(maxsplit=1)
                if len(parts) < 2 or not parts[1]:
                    print("Please specify a room label, e.g. 'enter archive'.")
                    continue
                room_label = parts[1]
                next_room = self.current_floor.get_room(room_label)
                if next_room:
                    self.current_room = next_room
                    self.items = self.current_room.enter_room(self.items, self.command_handler)
                else:
                    print("There is no such room...")
                continue

            # 4) Quick 'look' on the floor to reprint orientation
            if action in {"look"}:
                # Just loop to re-render the floor panel & orientation
                continue

            # 5) Unknown command
            print(f"Unknown command! Type '{EXIT_COMMAND}' to stop the game or 'help' for help.")


if __name__ == "__main__":
    adventure = ZDDAdventure()
    adventure.play()
