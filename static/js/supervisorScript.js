const socket = io("http://localhost:5000");

// On connect, identify as supervisor
socket.on('connect', () => {
    socket.emit('join', {
        user_id: "supervisor123",
        role: "supervisor"
    });
});

function assignTask() {
    const supplierId = document.getElementById('supplierId').value;
    const task = document.getElementById('task').value;
    assignTaskToSupplier(supplierId, task);
}

// Example function to assign task to a supplier
function assignTaskToSupplier(supplierId, taskDescription) {
    socket.emit('assign_task', {
        supplier_id: supplierId,
        task: taskDescription
    });
}

// Optional: receive acknowledgment or broadcast
socket.on('user_connected', (data) => {
    console.log(data.message);
});