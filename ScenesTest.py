class Stage:
    def __init__(self, Name, Requirements=None):
        self.Name = Name
        self.Requirements = Requirements if Requirements else []

    def AreRequirementsMet(self, completed_stages):
        """Check if the stage's requirements are met based on completed stages."""
        return all(req in completed_stages for req in self.Requirements)

# List to store stages that have been completed
completed_stages = []

# Catalog of stages, including dependencies
stage_catalog = [
    Stage("Prologue"),
    Stage("Act I", ["Prologue"]),
    Stage("Act II", ["Prologue", "Act I"]),
    Stage("Post Act II: Branch A Part I", ["Prologue", "Act I", "Act II"]),
    Stage("Post Act II: Branch B", ["Prologue", "Act I", "Act II"]),
    Stage("Post Act II: Branch A Part II", ["Prologue", "Act I", "Act II", "Post Act II: Branch A Part I"]),
    Stage("Quest #1", ["Prologue", "Act I"]),
    Stage("Quest #2", ["Prologue", "Act I"]),
    Stage("Quest #3", ["Prologue", "Act I"]),
    Stage("Quest #4", ["Prologue", "Act I", "Quest #1"]),
    Stage("Quest #5", ["Prologue", "Act I", "Quest #2"]),
    Stage("Quest #6", ["Prologue", "Act I", "Act II"]),
    Stage("Quest #7", ["Prologue", "Act I", "Act II"]),
    Stage("Quest #8", ["Prologue", "Act I", "Act II", "Quest #3"]),
    Stage("Quest #9", ["Prologue", "Act I", "Act II", "Quest #6"]),
    Stage("Quest #10", ["Prologue", "Act I", "Act II", "Quest #9"]),
]

uncompleted_stages = [stage.Name for stage in stage_catalog]
available_stages = []

# Function to show available stages based on completed ones
def show_available_stages(completed_stages):
    available_stages = [stage.Name for stage in stage_catalog if stage.AreRequirementsMet(completed_stages)]
    return available_stages

# Example of adding completed stages and checking availability
# completed_stages.append("Prologue")
# completed_stages.append("Act I")
# completed_stages.append("Act II")

# Print stages that are now available
print("Available stages:", show_available_stages(completed_stages))
while True:
    print("Available stages:")
    available_stages = show_available_stages(completed_stages)
    for i, stage in enumerate(available_stages):
        print(f"{i + 1} <- {stage}")
    choice = int(input("Select: "))
    chosen_stage = available_stages[choice - 1]
    if chosen_stage not in completed_stages:
        completed_stages.append(chosen_stage)
