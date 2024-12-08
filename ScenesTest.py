# Catalog of stages, including dependencies
class Stage:
    def __init__(self, ID, Name, Requirements=None):
        self.ID = ID  # Unique identifier for each stage
        self.Name = Name
        self.Requirements = Requirements if Requirements else []

    def AreRequirementsMet(self, completed_stages):
        """Check if the stage's requirements are met based on completed stages."""
        return all(stage.Name in completed_stages for stage in stage_catalog if stage.ID in self.Requirements)

# List to store stages that have been completed
completed_stages = []

# Catalog of stages, now with IDs
stage_catalog = [
    Stage(1, "Prologue"),
    Stage(2, "Act I", [1]),
    Stage(3, "Act II", [1, 2]),
    Stage(4, "Post Act II: Branch A Part I", [1, 2, 3]),
    Stage(5, "Post Act II: Branch B", [1, 2, 3]),
    Stage(6, "Post Act II: Branch A Part II", [1, 2, 3, 4]),
    Stage(7, "Quest #1", [1, 2]),
    Stage(8, "Quest #2", [1, 2]),
    Stage(9, "Quest #3", [1, 2]),
    Stage(10, "Quest #4", [1, 2, 7]),
    Stage(11, "Quest #5", [1, 2, 8]),
    Stage(12, "Quest #6", [1, 2, 3]),
    Stage(13, "Quest #7", [1, 2, 3]),
    Stage(14, "Quest #8", [1, 2, 3, 9]),
    Stage(15, "Quest #9", [1, 2, 3, 12]),
    Stage(16, "Quest #10", [1, 2, 3, 15]),
]

# Function to show available stages based on completed ones
def show_available_stages(completed_stages):
    available_stages = [stage.Name for stage in stage_catalog if stage.AreRequirementsMet(completed_stages)]
    return available_stages

# Main loop for user interaction
while True:
    available_stages = show_available_stages(completed_stages)
    if not available_stages:
        print("No available stages to complete.")
        break
    
    print("\nAvailable stages:")
    for i, stage in enumerate(available_stages):
        print(f"{i + 1} <- {stage}")
    
    try:
        choice = int(input("Select a stage to complete (or 0 to exit): "))
        if choice == 0:
            break
        chosen_stage = available_stages[choice - 1]
        
        if chosen_stage not in completed_stages:
            completed_stages.append(chosen_stage)
            print(f"Stage '{chosen_stage}' marked as completed.")
        else:
            print(f"Stage '{chosen_stage}' is already completed.")
    except (ValueError, IndexError):
        print("Invalid choice. Please select a valid stage number.")
    
    # Display completed stages for user
    print("\nCompleted stages:", completed_stages)
