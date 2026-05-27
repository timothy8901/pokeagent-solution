#!/usr/bin/env python3
"""
Milestone Manager for tracking Pokemon Emerald progression
Follows SimpleAgent's Objective pattern with descriptions
"""

class MilestoneManager:
    """Manages complete milestone order with descriptions"""

    # Complete milestone list with descriptions (from SimpleAgent objectives)
    ALL_MILESTONES = [
        # Phase 1: Game Initialization
        {
            "id": "GAME_RUNNING",
            "description": "Complete title sequence and begin the game",
            "category": "system",
            "condition": "state is not None"
        },
        {
            "id": "PLAYER_NAME_SET",
            "description": "Player has chosen their character name",
            "category": "intro",
            "condition": "state.get('player', {}).get('name', '').strip() not in ['', 'UNKNOWN', 'PLAYER']"
        },
        {
            "id": "INTRO_CUTSCENE_COMPLETE",
            "description": "Complete intro cutscene with moving van",
            "category": "intro",
            "condition": "'MOVING_VAN' in str(state.get('player', {}).get('location', '')).upper()"
        },

        # Phase 2: Tutorial & Starting Town
        {
            "id": "LITTLEROOT_TOWN",
            "description": "Arrive at Littleroot Town",
            "category": "location",
            "condition": "'LITTLEROOT' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "PLAYER_HOUSE_ENTERED",
            "description": "Enter player's house for the first time",
            "category": "location",
            "condition": "'LITTLEROOT TOWN BRENDANS HOUSE 1F' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "PLAYER_BEDROOM",
            "description": "Go upstairs to player's bedroom",
            "category": "location",
            "condition": "'LITTLEROOT TOWN BRENDANS HOUSE 2F' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "RIVAL_HOUSE",
            "description": "Visit May's house next door",
            "category": "location",
            "condition": "'LITTLEROOT TOWN MAYS HOUSE 1F' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "RIVAL_BEDROOM",
            "description": "Visit May's bedroom on the second floor",
            "category": "location",
            "condition": "'LITTLEROOT TOWN MAYS HOUSE 2F' in str(state.get('player', {}).get('location', '')).upper()"
        },

        # Phase 3: Professor Birch & Starter
        {
            "id": "ROUTE_101",
            "description": "Travel to Route 101",
            "category": "location",
            "condition": "'ROUTE_101' in str(state.get('player', {}).get('location', '')).upper() or 'ROUTE 101' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "STARTER_CHOSEN",
            "description": "Choose starter Pokemon",
            "category": "pokemon",
            "condition": "len(state.get('player', {}).get('party', [])) >= 1 and any(p.get('species_name', '').strip() for p in state.get('player', {}).get('party', []))"
        },
        {
            "id": "BIRCH_LAB_VISITED",
            "description": "Visit Professor Birch's lab",
            "category": "location",
            "condition": "'LITTLEROOT TOWN PROFESSOR BIRCHS LAB' in str(state.get('player', {}).get('location', '')).upper()"
        },

        # Phase 4: Rival Battle
        {
            "id": "OLDALE_TOWN",
            "description": "Arrive at Oldale Town",
            "category": "location",
            "condition": "'OLDALE' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "ROUTE_103",
            "description": "Travel to Route 103 and battle with May",
            "category": "location",
            "condition": "'ROUTE_103' in str(state.get('player', {}).get('location', '')).upper() or 'ROUTE 103' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "RECEIVED_POKEDEX",
            "description": "Visit Birch's lab to receive Pokedex from Professor Birch",
            "category": "item",
            "condition": "'LITTLEROOT TOWN PROFESSOR BIRCHS LAB' in str(state.get('player', {}).get('location', '')).upper()"
        },

        # Phase 5: Route 102 & Petalburg
        {
            "id": "ROUTE_102",
            "description": "Travel to Route 102",
            "category": "location",
            "condition": "'ROUTE_102' in str(state.get('player', {}).get('location', '')).upper() or 'ROUTE 102' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "PETALBURG_CITY",
            "description": "Arrive at Petalburg City",
            "category": "location",
            "condition": "'PETALBURG' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "DAD_FIRST_MEETING",
            "description": "Meet Dad at Petalburg Gym",
            "category": "story",
            "condition": "'PETALBURG CITY GYM' in str(state.get('player', {}).get('location', '')).upper() or 'PETALBURG_CITY_GYM' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "GYM_EXPLANATION",
            "description": "Receive gym explanation from Dad",
            "category": "story",
            "condition": "'PETALBURG CITY GYM' in str(state.get('player', {}).get('location', '')).upper() or 'PETALBURG_CITY_GYM' in str(state.get('player', {}).get('location', '')).upper()"
        },

        # Phase 6: Road to Rustboro
        {
            "id": "ROUTE_104_SOUTH",
            "description": "Travel to Route 104 (South)",
            "category": "location",
            "condition": "'ROUTE_104' in str(state.get('player', {}).get('location', '')).upper() or 'ROUTE 104' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "PETALBURG_WOODS",
            "description": "Navigate through Petalburg Woods",
            "category": "location",
            "condition": "'PETALBURG_WOODS' in str(state.get('player', {}).get('location', '')).upper() or 'PETALBURG WOODS' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "TEAM_AQUA_GRUNT_DEFEATED",
            "description": "Defeat Team Aqua grunt",
            "category": "battle",
            "condition": "('PETALBURG_WOODS' in str(state.get('player', {}).get('location', '')).upper() or 'PETALBURG WOODS' in str(state.get('player', {}).get('location', '')).upper()) and state.get('player', {}).get('position', {}).get('y') == 23 and state.get('player', {}).get('position', {}).get('x') in [26, 27]"
        },
        {
            "id": "ROUTE_104_NORTH",
            "description": "Travel to Route 104 (North)",
            "category": "location",
            "condition": "'ROUTE_104' in str(state.get('player', {}).get('location', '')).upper() or 'ROUTE 104' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "RUSTBORO_CITY",
            "description": "Arrive at Rustboro City",
            "category": "location",
            "condition": "'RUSTBORO' in str(state.get('player', {}).get('location', '')).upper()"
        },

        # Phase 7: First Gym
        {
            "id": "RUSTBORO_GYM_ENTERED",
            "description": "Enter Rustboro Gym",
            "category": "location",
            "condition": "'RUSTBORO_GYM' in str(state.get('player', {}).get('location', '')).upper() or 'RUSTBORO CITY GYM' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "ROXANNE_DEFEATED",
            "description": "Defeat Gym Leader Roxanne",
            "category": "battle",
            "condition": "(len(state.get('game', {}).get('badges', [])) >= 1 or any('Stone' in str(b) for b in state.get('game', {}).get('badges', []))) if isinstance(state.get('game', {}).get('badges', []), list) else state.get('game', {}).get('badges', 0) >= 1"
        },
        {
            "id": "FIRST_GYM_COMPLETE",
            "description": "Receive Stone Badge (first gym badge)",
            "category": "badge",
            "condition": "((len(state.get('game', {}).get('badges', [])) >= 1 or any('Stone' in str(b) for b in state.get('game', {}).get('badges', []))) if isinstance(state.get('game', {}).get('badges', []), list) else state.get('game', {}).get('badges', 0) >= 1) and 'GYM' not in str(state.get('player', {}).get('location', '')).upper()"
        },
        # Phase 8: Route to Dewford
        {
            "id": "RUSTBORO_CENTER",
            "description": "Heal at Rustboro Pokemon Center before heading south",
            "category": "heal",
            "condition": "'RUSTBORO' in str(state.get('player', {}).get('location', '')).upper() and 'CENTER' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "ROUTE_109_SOUTH",
            "description": "Travel south on Route 109 to Dewford Town",
            "category": "location",
            "condition": "'DEWFORD' in str(state.get('player', {}).get('location', '')).upper() or 'ROUTE_109' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "DEWFORD_TOWN_ARRIVED",
            "description": "Arrive at Dewford Town",
            "category": "location",
            "condition": "'DEWFORD TOWN' in str(state.get('player', {}).get('location', '')).upper()"
        },

        # Phase 9: Second Gym - Dewford (Wattson - Electric)
        {
            "id": "DEWFORD_GYM_ENTERED",
            "description": "Enter Dewford Gym (Thunder Mountain)",
            "category": "location",
            "condition": "'DEWFORD_TOWN_GYM' in str(state.get('player', {}).get('location', '')).upper() or 'DEWFORD GYM' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "WATTSON_DEFEATED",
            "description": "Defeat Gym Leader Wattson",
            "category": "battle",
            "condition": "(len(state.get('game', {}).get('badges', [])) >= 2) if isinstance(state.get('game', {}).get('badges', []), list) else state.get('game', {}).get('badges', 0) >= 2"
        },
        {
            "id": "SECOND_GYM_COMPLETE",
            "description": "Receive Dynamo Badge (second gym badge)",
            "category": "badge",
            "condition": "((len(state.get('game', {}).get('badges', [])) >= 2) if isinstance(state.get('game', {}).get('badges', []), list) else state.get('game', {}).get('badges', 0) >= 2) and 'GYM' not in str(state.get('player', {}).get('location', '')).upper()"
        },

        # Phase 10: Route to Lavaridge
        {
            "id": "ROUTE_109_NORTH",
            "description": "Travel north on Route 109 toward Lavaridge",
            "category": "location",
            "condition": "'ROUTE_109' in str(state.get('player', {}).get('location', '')).upper() or 'HOT_SPRINGS' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "LAVARIDGE_TOWN_ARRIVED",
            "description": "Arrive at Lavaridge Town",
            "category": "location",
            "condition": "'LAVARIDGE' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "LAVARIDGE_GYM_ENTERED",
            "description": "Enter Lavaridge Gym (Volcanic Cave)",
            "category": "location",
            "condition": "'LAVARIDGE_TOWN_GYM' in str(state.get('player', {}).get('location', '')).upper() or 'LAVARIDGE GYM' in str(state.get('player', {}).get('location', '')).upper()"
        },

        # Phase 11: Third Gym - Lavaridge (Flannery - Fire)
        {
            "id": "FLANNERY_DEFEATED",
            "description": "Defeat Gym Leader Flannery",
            "category": "battle",
            "condition": "(len(state.get('game', {}).get('badges', [])) >= 3) if isinstance(state.get('game', {}).get('badges', []), list) else state.get('game', {}).get('badges', 0) >= 3"
        },
        {
            "id": "THIRD_GYM_COMPLETE",
            "description": "Receive Heat Badge (third gym badge)",
            "category": "badge",
            "condition": "((len(state.get('game', {}).get('badges', [])) >= 3) if isinstance(state.get('game', {}).get('badges', []), list) else state.get('game', {}).get('badges', 0) >= 3) and 'GYM' not in str(state.get('player', {}).get('location', '')).upper()"
        },

        # Phase 12: Route to Pacifidlog
        {
            "id": "ROUTE_124_TO_PACIFIDLOG",
            "description": "Travel via Route 124 to Pacifidlog Town (boat route)",
            "category": "location",
            "condition": "'PACIFIDLOG' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "PACIFIDLOG_GYM_ENTERED",
            "description": "Enter Pacifidlog Gym (Norman - requires Surf)",
            "category": "location",
            "condition": "'PACIFIDLOG_TOWN_GYM' in str(state.get('player', {}).get('location', '')).upper() or 'PACIFIDLOG GYM' in str(state.get('player', {}).get('location', '')).upper()"
        },

        # Phase 13: Fourth Gym - Pacifidlog (Norman - Normal)
        {
            "id": "NORMAN_DEFEATED",
            "description": "Defeat Gym Leader Norman (also known as the Player's Dad)",
            "category": "battle",
            "condition": "(len(state.get('game', {}).get('badges', [])) >= 4) if isinstance(state.get('game', {}).get('badges', []), list) else state.get('game', {}).get('badges', 0) >= 4"
        },
        {
            "id": "FOURTH_GYM_COMPLETE",
            "description": "Receive Balance Badge (fourth gym badge)",
            "category": "badge",
            "condition": "((len(state.get('game', {}).get('badges', [])) >= 4) if isinstance(state.get('game', {}).get('badges', []), list) else state.get('game', {}).get('badges', 0) >= 4) and 'GYM' not in str(state.get('player', {}).get('location', '')).upper()"
        },

        # Phase 14: Route to Fortree
        {
            "id": "ROUTE_119_TO_FOR TREE",
            "description": "Travel via Routes 119 and 120 to Fortree City (via tree top bridge)",
            "category": "location",
            "condition": "'FORTREE' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "FORTREE_GYM_ENTERED",
            "description": "Enter Fortree Gym (bird-themed, high up in trees)",
            "category": "location",
            "condition": "'FORTREE_CITY_GYM' in str(state.get('player', {}).get('location', '')).upper() or 'FORTREE GYM' in str(state.get('player', {}).get('location', '')).upper()"
        },

        # Phase 15: Fifth Gym - Fortree (Winona - Flying)
        {
            "id": "WINONA_DEFEATED",
            "description": "Defeat Gym Leader Winona",
            "category": "battle",
            "condition": "(len(state.get('game', {}).get('badges', [])) >= 5) if isinstance(state.get('game', {}).get('badges', []), list) else state.get('game', {}).get('badges', 0) >= 5"
        },
        {
            "id": "FIFTH_GYM_COMPLETE",
            "description": "Receive Feather Badge (fifth gym badge)",
            "category": "badge",
            "condition": "((len(state.get('game', {}).get('badges', [])) >= 5) if isinstance(state.get('game', {}).get('badges', []), list) else state.get('game', {}).get('badges', 0) >= 5) and 'GYM' not in str(state.get('player', {}).get('location', '')).upper()"
        },

        # Phase 16: Route to Mossdeep
        {
            "id": "ROUTE_123_TO_MOSSDEEP",
            "description": "Travel via Routes 123 and 124 to Mossdeep City",
            "category": "location",
            "condition": "'MOSSDEEP' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "MOSSDEEP_GYM_ENTERED",
            "description": "Enter Mossdeep Gym (space-themed, underwater)",
            "category": "location",
            "condition": "'MOSSDEEP_CITY_GYM' in str(state.get('player', {}).get('location', '')).upper() or 'MOSSDEEP GYM' in str(state.get('player', {}).get('location', '')).upper()"
        },

        # Phase 17: Sixth Gym - Mossdeep (Tate & Liza - Psychic)
        {
            "id": "TATE_LIZA_DEFEATED",
            "description": "Defeat Gym Leaders Tate & Liza (twin gym leaders)",
            "category": "battle",
            "condition": "(len(state.get('game', {}).get('badges', [])) >= 6) if isinstance(state.get('game', {}).get('badges', []), list) else state.get('game', {}).get('badges', 0) >= 6"
        },
        {
            "id": "SIXTH_GYM_COMPLETE",
            "description": "Receive Mind Badge (sixth gym badge)",
            "category": "badge",
            "condition": "((len(state.get('game', {}).get('badges', [])) >= 6) if isinstance(state.get('game', {}).get('badges', []), list) else state.get('game', {}).get('badges', 0) >= 6) and 'GYM' not in str(state.get('player', {}).get('location', '')).upper()"
        },

        # Phase 18: Route to Sootopolis
        {
            "id": "ROUTE_126_TO_SOETOPOLIS",
            "description": "Travel via Routes 126, 127, and 128 to Sootopolis City (requires Surf)",
            "category": "location",
            "condition": "'SOETOPOLIS' in str(state.get('player', {}).get('location', '')).upper() or 'SOOTOPOLIS' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "SOETOPOLIS_GYM_ENTERED",
            "description": "Enter Sootopolis Gym (underwater, water-themed)",
            "category": "location",
            "condition": "'SOETOPOLIS_CITY_GYM' in str(state.get('player', {}).get('location', '')).upper() or 'SOOTOPOLIS GYM' in str(state.get('player', {}).get('location', '')).upper()"
        },

        # Phase 19: Seventh Gym - Sootopolis (Juan - Water)
        {
            "id": "JUAN_DEFEATED",
            "description": "Defeat Gym Leader Juan",
            "category": "battle",
            "condition": "(len(state.get('game', {}).get('badges', [])) >= 7) if isinstance(state.get('game', {}).get('badges', []), list) else state.get('game', {}).get('badges', 0) >= 7"
        },
        {
            "id": "SEVENTH_GYM_COMPLETE",
            "description": "Receive Rain Badge (seventh gym badge)",
            "category": "badge",
            "condition": "((len(state.get('game', {}).get('badges', [])) >= 7) if isinstance(state.get('game', {}).get('badges', []), list) else state.get('game', {}).get('badges', 0) >= 7) and 'GYM' not in str(state.get('player', {}).get('location', '')).upper()"
        },

        # Phase 20: Pokémon League
        {
            "id": "ROUTE_TO_LEAGUE",
            "description": "Travel via Routes 131, 132, and 133 to the Pokémon League",
            "category": "location",
            "condition": "'POKEMON_LEAGUE' in str(state.get('player', {}).get('location', '')).upper() or 'HOENN LEAGUE' in str(state.get('player', {}).get('location', '')).upper()"
        },
        {
            "id": "LEAGUE_LOCKER",
            "description": "Use the League locker to heal and switch Pokemon",
            "category": "action",
            "condition": "'POKEMON_LEAGUE' in str(state.get('player', {}).get('location', '')).upper() and 'LOCKER' in str(state.get('game', {}).get('dialog', '')).upper()"
        },

        # Phase 21: Elite Four
        {
            "id": "ELITE_SIDNEY",
            "description": "Defeat Elite Four member Sidney (Dark type)",
            "category": "battle",
            "condition": "'ELITE_FOUR' in str(state.get('player', {}).get('location', '')).upper() and 'SIDNEY' in str(state.get('game', {}).get('dialog', '')).upper()"
        },
        {
            "id": "ELITE_PHOEBE",
            "description": "Defeat Elite Four member Phoebe (Ghost type)",
            "category": "battle",
            "condition": "'ELITE_FOUR' in str(state.get('player', {}).get('location', '')).upper() and 'PHOEBE' in str(state.get('game', {}).get('dialog', '')).upper()"
        },
        {
            "id": "ELITE_GLACIA",
            "description": "Defeat Elite Four member Glacia (Ice type)",
            "category": "battle",
            "condition": "'ELITE_FOUR' in str(state.get('player', {}).get('location', '')).upper() and 'GLACIA' in str(state.get('game', {}).get('dialog', '')).upper()"
        },
        {
            "id": "ELITE_DRAKE",
            "description": "Defeat Elite Four member Drake (Dragon type)",
            "category": "battle",
            "condition": "'ELITE_FOUR' in str(state.get('player', {}).get('location', '')).upper() and 'DRAKE' in str(state.get('game', {}).get('dialog', '')).upper()"
        },

        # Phase 22: Champion
        {
            "id": "CHAMPION_WALLACE",
            "description": "Defeat Champion Wallace to complete the game!",
            "category": "battle",
            "condition": "'CHAMPION' in str(state.get('player', {}).get('location', '')).upper() or 'HALL_OF_FAME' in str(state.get('player', {}).get('location', '')).upper() or 'WALLACE' in str(state.get('game', {}).get('dialog', '')).upper()"
        },
        {
            "id": "GAME_COMPLETE",
            "description": "Game complete! Hall of Fame achieved.",
            "category": "system",
            "condition": "'HALL_OF_FAME' in str(state.get('player', {}).get('location', '')).upper()"
        }
    ]

    def __init__(self):
        """Initialize milestone manager with lookup dict"""
        # Build lookup dict for quick access by ID
        self._milestone_dict = {m["id"]: m for m in self.ALL_MILESTONES}

        # Custom milestones (instance-level, not shared between instances)
        self.custom_milestones = []

    def add_custom_milestone(
        self,
        milestone_id: str,
        description: str,
        insert_after: str,
        check_fn: callable,
        category: str = "custom"
    ):
        """
        Add a custom milestone to this manager instance

        Args:
            milestone_id: Unique milestone ID
            description: Human-readable description for LLM
            insert_after: ID of milestone to insert after
            check_fn: Completion check function (game_state, action) -> bool
            category: Category for UI display
        """
        self.custom_milestones.append({
            "id": milestone_id,
            "description": description,
            "category": category,
            "insert_after": insert_after,
            "check_fn": check_fn
        })

    def get_ordered_milestones(self) -> list:
        """
        Get all milestones in correct order

        Algorithm:
        1. Add all server milestones first (in registration order)
        2. Insert custom milestones in order at their insert_after positions

        This is simple and preserves registration order.

        Returns:
            List of milestone dicts with id, description, category, insert_after
        """
        if not self.custom_milestones:
            return []

        # Define server categories
        server_categories = {'location', 'task', 'story', 'badge', 'event', 'item', 'pokemon', 'intro', 'system'}

        # Step 1: Add all server milestones in registration order
        result = []
        for milestone in self.custom_milestones:
            category = milestone.get("category", "")
            if category in server_categories:
                result.append({
                    "id": milestone["id"],
                    "description": milestone["description"],
                    "category": category,
                    "insert_after": milestone.get("insert_after")
                })

        # Step 2: Insert custom milestones at their insert_after positions
        # Use multiple passes to handle chains (e.g., A→B→C where B is also custom)
        remaining_customs = []
        for milestone in self.custom_milestones:
            category = milestone.get("category", "")
            if category not in server_categories:
                remaining_customs.append({
                    "id": milestone["id"],
                    "description": milestone["description"],
                    "category": category,
                    "insert_after": milestone.get("insert_after")
                })

        # Process customs in multiple passes
        max_iterations = len(remaining_customs) + 1
        for _ in range(max_iterations):
            if not remaining_customs:
                break

            newly_added = []

            for custom in remaining_customs:
                insert_after_id = custom.get("insert_after")

                # Find insert_after position in result
                found = False
                for i, m in enumerate(result):
                    if m["id"] == insert_after_id:
                        # Insert right after this position
                        result.insert(i + 1, custom)
                        newly_added.append(custom)
                        found = True
                        break

                if not found and insert_after_id is None:
                    # No parent, add at end
                    result.append(custom)
                    newly_added.append(custom)

            # Remove added customs
            for added in newly_added:
                remaining_customs.remove(added)

            # Stop if no progress
            if not newly_added:
                # Add remaining at end (orphaned customs)
                for custom in remaining_customs:
                    result.append(custom)
                break

        return result

    def get_custom_check_fn(self, milestone_id: str):
        """
        Get the check function for a custom milestone

        Args:
            milestone_id: Milestone ID

        Returns:
            Check function or None if not a custom milestone
        """
        for custom in self.custom_milestones:
            if custom["id"] == milestone_id:
                return custom["check_fn"]
        return None

    def get_milestone_info(self, milestone_id: str) -> dict:
        """
        Get full milestone info by ID (checks both base and custom)

        Args:
            milestone_id: Milestone ID string

        Returns:
            Dict with id, description, category or default if not found
        """
        # Check base milestones first
        if milestone_id in self._milestone_dict:
            return self._milestone_dict[milestone_id]

        # Check custom milestones
        for custom in self.custom_milestones:
            if custom["id"] == milestone_id:
                return {
                    "id": custom["id"],
                    "description": custom["description"],
                    "category": custom["category"]
                }

        # Not found
        return {
            "id": milestone_id,
            "description": "Unknown milestone",
            "category": "unknown"
        }

    def get_next_milestone(self, completed_milestones: dict) -> str:
        """
        Get next uncompleted milestone ID (includes custom milestones)

        Args:
            completed_milestones: Dict like {"GAME_RUNNING": {"completed": True, ...}}
                                  Only contains completed milestones

        Returns:
            Next milestone ID (string) or None if all complete
        """
        # Use ordered milestones which includes custom milestones
        ordered = self.get_ordered_milestones()

        for milestone in ordered:
            milestone_id = milestone["id"]
            # If not in dict, it's not completed yet
            if milestone_id not in completed_milestones:
                return milestone_id
            # If in dict but completed=False, also not completed
            if not completed_milestones[milestone_id].get('completed', False):
                return milestone_id
        return None  # All completed

    def get_next_milestone_info(self, completed_milestones: dict) -> dict:
        """
        Get full info dict for next milestone

        Args:
            completed_milestones: Dict of completed milestones

        Returns:
            Milestone info dict or None if all complete
        """
        next_id = self.get_next_milestone(completed_milestones)
        if next_id:
            return self.get_milestone_info(next_id)
        return None

    def get_next_milestone_index(self, completed_milestones: dict) -> int:
        """
        Get index of next milestone in ALL_MILESTONES list

        Args:
            completed_milestones: Dict of completed milestones

        Returns:
            Index (0-based) or len(ALL_MILESTONES) if all complete
        """
        next_id = self.get_next_milestone(completed_milestones)
        if next_id:
            return next(i for i, m in enumerate(self.ALL_MILESTONES) if m["id"] == next_id)
        return len(self.ALL_MILESTONES)  # All complete

    def get_all_with_status(self, completed_milestones: dict) -> list:
        """
        Get all milestones with completion status and descriptions

        Args:
            completed_milestones: Dict of completed milestones

        Returns:
            List of dicts with:
            - id: milestone ID
            - name: milestone ID (for backward compatibility)
            - description: human-readable description
            - category: milestone category
            - completed: bool
            - index: position in list
            - timestamp: completion timestamp or None
        """
        result = []
        for i, milestone in enumerate(self.ALL_MILESTONES):
            milestone_id = milestone["id"]
            is_completed = milestone_id in completed_milestones and \
                          completed_milestones[milestone_id].get('completed', False)

            result.append({
                "id": milestone_id,
                "name": milestone_id,  # For backward compatibility
                "description": milestone["description"],
                "category": milestone["category"],
                "completed": is_completed,
                "index": i,
                "timestamp": completed_milestones.get(milestone_id, {}).get('timestamp') if is_completed else None
            })
        return result

    def get_total_count(self) -> int:
        """Get total number of milestones"""
        return len(self.ALL_MILESTONES)
