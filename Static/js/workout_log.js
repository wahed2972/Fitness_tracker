document.addEventListener("DOMContentLoaded", function () {
    const calendarElement = document.getElementById("calendar");
    const workoutDisplay = document.getElementById("workout-display");
    let workoutData = [];

    const calendar = new FullCalendar.Calendar(calendarElement, {
        initialView: "dayGridMonth",
        events: workoutData,
        eventClick: function (info) {
            const workout = info.event;
            handleWorkoutDialog(workout);
            fetchWorkoutsAndUpdateCalendar();
        },
        contentHeight: "auto",
        aspectRatio: 1.5,
        dateClick: function (info) {
            const selectedDate = info.dateStr;
            displayWorkoutsForDate(selectedDate);
            fetchWorkoutsAndUpdateCalendar();
        },
    });

    function fetchWorkoutsAndUpdateCalendar() {
        $.ajax({
            url: "/get_workouts",
            type: "GET",
            success: function (data) {
                console.log("Received data:", data);
                // Clear existing events on the calendar
                calendar.removeAllEvents();

                // Populate workoutData array with the retrieved data
                workoutData = data.workouts;

                // Update FullCalendar events
                workoutData.forEach(function (workout) {
                    calendar.addEvent({
                        id: workout.id,
                        title: `${workout.exercise_name}: ${workout.sets} sets, ${workout.reps} reps, ${workout.weight} lbs`,
                        start: workout.date,
                        extendedProps: {
                            exercise_name: workout.exercise_name,
                            sets: workout.sets,
                            reps: workout.reps,
                            weight: workout.weight,
                        },
                    });
                });
            },
            error: function (error) {
                console.error("Error fetching workouts:", error);
            },
        });
    }

    calendar.render();
    fetchWorkoutsAndUpdateCalendar();

    // Handle form submission
    const workoutForm = document.getElementById("workout-form");
    workoutForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const exerciseName = document.getElementById("exercise-name").value;
        const sets = document.getElementById("sets").value;
        const reps = document.getElementById("reps").value;
        const weight = document.getElementById("weight").value;
        const workoutDate = document.getElementById("workout-date").value;

        if (!exerciseName || !sets || !reps || !weight || !workoutDate) {
            alert("Please fill in all the workout details.");
            return;
        }

        const currentDate = new Date();
        currentDate.setHours(0, 0, 0, 0);

        const selectedDate = new Date(workoutDate);
        selectedDate.setHours(0, 0, 0, 0);

        if (selectedDate > currentDate) {
            alert("You can't add workouts for future days.");
            return;
        }

        const workoutEntry = `${exerciseName}: ${sets} sets, ${reps} reps,${weight} lbs`;
        const workoutId = new Date().getTime();

        // Add the workout to workoutData
        workoutData.push({ id: workoutId, date: workoutDate, details: workoutEntry });

        // Add the workout to the calendar
        calendar.addEvent({
            id: workoutId,
            title: workoutEntry,
            start: workoutDate,
            extendedProps: {
                exerciseName: exerciseName,
                sets: sets,
                reps: reps,
                weight: weight,
            },
        });

        // Clear the form
        document.getElementById("exercise-name").value = "";
        document.getElementById("sets").value = "";
        document.getElementById("reps").value = "";
        document.getElementById("weight").value = "";
        document.getElementById("workout-date").value = "";

        $.ajax({
            url: "/add_workout",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                exercise_name: exerciseName,
                sets: sets,
                reps: reps,
                weight: weight,
                date: workoutDate
            }),
            success: function (data) {
                console.log(data.message);
                fetchWorkoutsAndUpdateCalendar();
            },
            error: function (error) {
                console.error("Error adding workout:", error);
            }
        });
        function fetchWorkoutsAndUpdateCalendar() {
            $.ajax({
                url: "/get_workouts",
                type: "GET",
                success: function (data) {
                    console.log("Received data:", data);
                    // Clear existing events on the calendar
                    calendar.removeAllEvents();
        
                    // Populate workoutData array with the retrieved data
                    workoutData = data.workouts;
        
                    // Update FullCalendar events
                    workoutData.forEach(function (workout) {
                        calendar.addEvent({
                            id: workout.id,
                            title: `${workout.exercise_name}: ${workout.sets} sets, ${workout.reps} reps, ${workout.weight} lbs`,
                            start: workout.date,
                            extendedProps: {
                                exercise_name:workout.exercise_name,
                                sets: workout.sets,
                                reps: workout.reps,
                                weight: workout.weight
                            },
                        });
                    });
                },
                error: function (error) {
                    console.error("Error fetching workouts:", error);
                },
            });
        }
    });

    // Function to handle workout dialog (Edit and Delete)
    
    function handleWorkoutDialog(workout) {
        const dialog = document.createElement("div");
        dialog.classList.add("modal"); // Add the modal class

    // Create Edit button
    const editButton = document.createElement("button");
    editButton.textContent = "Edit";
    editButton.addEventListener("click", function () {
        editWorkout(workout);
        $(dialog).dialog("close");
    });

    // Create Delete button
    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", function () {
        deleteWorkout(workout);
        $(dialog).dialog("close");
    });

    dialog.appendChild(editButton);
    dialog.appendChild(deleteButton);

    $(dialog).dialog();
    
}

// Function to edit a workout
function editWorkout(workout) {
    const editDialog = document.createElement("div");
    editDialog.title = "Edit Workout";
    const exerciseNameInput = document.createElement("input");
    
    exerciseNameInput.value = workout.extendedProps.exerciseName;
    const setsInput = document.createElement("input");
    setsInput.value = workout.extendedProps.sets;
    const repsInput = document.createElement("input");
    repsInput.value = workout.extendedProps.reps;
    const weightInput = document.createElement("input");
    weightInput.value = workout.extendedProps.weight;

    editDialog.appendChild(document.createTextNode("Exercise Name: "));
    editDialog.appendChild(exerciseNameInput);
    editDialog.appendChild(document.createElement("br"));

    editDialog.appendChild(document.createTextNode("Sets: "));
    editDialog.appendChild(setsInput);
    editDialog.appendChild(document.createElement("br"));

    editDialog.appendChild(document.createTextNode("Reps: "));
    editDialog.appendChild(repsInput);
    editDialog.appendChild(document.createElement("br"));

    editDialog.appendChild(document.createTextNode("Weight: "));
    editDialog.appendChild(weightInput);
    editDialog.appendChild(document.createElement("br"));

    const saveButton = document.createElement("button");
    saveButton.textContent = "Save";
    saveButton.addEventListener("click", function () {
        const updatedExerciseName = exerciseNameInput.value;
        const updatedSets = setsInput.value;
        const updatedReps = repsInput.value;
        const updatedWeight = weightInput.value;
        const updatedWorkoutEntry = `${updatedExerciseName}: ${updatedSets} sets, ${updatedReps} reps, ${updatedWeight} lbs`;

        // Update the calendar event
        workout.setExtendedProp("exerciseName", updatedExerciseName);
        workout.setExtendedProp("sets", updatedSets);
        workout.setExtendedProp("reps", updatedReps);
        workout.setExtendedProp("weight", updatedWeight);
        workout.setProp("title", updatedWorkoutEntry);

        // Update the workout display directly
        workoutDisplay.innerHTML = updatedWorkoutEntry;

        // Close the dialog
        $(editDialog).dialog("close");
    });

    const cancelButton = document.createElement("button");
    cancelButton.textContent = "Cancel";
    cancelButton.addEventListener("click", function () {
        // Close the dialog without saving changes
        $(editDialog).dialog("close");
    });

    editDialog.appendChild(saveButton);
    editDialog.appendChild(cancelButton);

    $(editDialog).dialog();
}
function createInput(id, value) {
    const input = document.createElement("input");
    input.type = "number";
    input.id = id;
    input.value = value;
    input.required = true;
    return input;
}

   // Function to delete a workout
function deleteWorkout(workout) {
    if (confirm("Are you sure you want to delete this workout?")) {
        const workoutId = workout.id;
        workout.remove();
        removeWorkoutData(workoutId);

        // Clear the workout display for the selected date
        const selectedDate = workout.date;

        // Filter workouts again for the selected date
        const workoutsForDate = workoutData.filter((workout) => workout.date === selectedDate);
        let displayHTML = "<h2>Workouts for " + selectedDate + "</h2>";

        if (workoutsForDate.length > 0) {
            displayHTML += "<ul>";
            workoutsForDate.forEach((workout) => {
                displayHTML += "<li>" + workout.details + "</li>";
            });
            displayHTML += "</ul>";
        } else {
            displayHTML += "<p>No workouts for this date.</p>";
        }

        workoutDisplay.innerHTML = displayHTML;
    }
}

// Function to display workouts for a selected date
function displayWorkoutsForDate(selectedDate) {
    const workoutsForDate = workoutData.filter((workout) => workout.date === selectedDate);
    let displayHTML = "<h2>Workouts for " + selectedDate + "</h2>";

    if (workoutsForDate.length > 0) {
        displayHTML += "<ul>";
        workoutsForDate.forEach((workout) => {
            displayHTML += "<li>" + workout.details + "</li>";
        });
        displayHTML += "</ul>";
    } else {
        displayHTML += "<p>No workouts for this date.</p>";
    }

    workoutDisplay.innerHTML = displayHTML;
}

    // Function to remove workout data
    function removeWorkoutData(workoutId) {
        workoutData = workoutData.filter((workout) => workout.id !== workoutId);
    }
    function hideWorkoutDialog() {
    const dialog = document.getElementById("edit-dialog");
    dialog.style.display = "none"; // Hide the dialog
}
// Function to display workouts for a selected date
    function displayWorkoutsForDate(selectedDate) {
        const workoutsForDate = workoutData.filter((workout) => workout.date === selectedDate);
        let displayHTML = "<h2>Workouts for " + selectedDate + "</h2>";

        if (workoutsForDate.length > 0) {
            displayHTML += "<ul>";
            workoutsForDate.forEach((workout) => {
                displayHTML += "<li>" + workout.details + "</li>";
            });
            displayHTML += "</ul>";
        } else {
            displayHTML += "<p>No workouts for this date.</p>";
        }

        workoutDisplay.innerHTML = displayHTML;
    }
});
