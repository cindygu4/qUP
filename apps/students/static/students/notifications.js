// Start with first notification
let counter = 1;

// Load notifications 10 at a time
const quantity = 10;

// When DOM loads, render the first 10 notifications
document.addEventListener('DOMContentLoaded', load);

// If scrolled to bottom, load the next 10 notifications
window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        load();
    }
};

// Load next set of notifications
function load() {

    // Set start and end notification numbers, and update counter
    const start = counter;
    const end = start + quantity - 1;
    counter = end + 1;

    // Get new notifications and add them
    fetch(`/student/notifications/?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data => {
        data.notifications.forEach(add_notification);
    })
};

// Add a new notification with given contents to DOM
function add_notification(contents) {

    // Create new notification
    const row = document.createElement('div');
    row.className = 'row';
    const first_col = document.createElement('div');
    first_col.className = 'col';
    const second_col = document.createElement('div');
    second_col.className = 'col';
    const notification_col = document.createElement('div');
    notification_col.className = 'col-10 col-md-6';
    const notification = document.createElement('div');
    notification.className = 'card mb-3';
    const card_body = document.createElement('div');
    card_body.className = 'card-body';
    const title = document.createElement('h5');
    title.className = 'card-title';
    title.innerHTML = `${contents['class_name']} - ${contents['queue_name']}`;
    const date_time = document.createElement('div');
    date_time.className = 'card-text';
    date_time.innerHTML = `${contents['date']} at ${contents['time']}`;
    const info = document.createElement('div');
    info.className = 'card-text';
    info.innerHTML = `${contents['content']}`;

    // adding all parts to the row element
    card_body.append(title);
    card_body.append(date_time);
    card_body.append(info);
    notification.append(card_body);
    notification_col.append(notification);
    row.append(first_col);
    row.append(notification_col);
    row.append(second_col);

    // Add all parts of the card to DOM
    document.querySelector('#notifications').append(row);
    console.log(contents);
};