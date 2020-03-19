// connect to Pusher
var pusher = new Pusher('fab32afad87f9a9d80a6', {
                        cluster: 'us3',
                        forceTLS: true
                        });
// subscribe to crypto channel
const channel = pusher.subscribe('crypto')
// listen for relevant events
channel.bind('data-updated', function(data) {
    const grid = JSON.parse(data.grid);
    Plotly.newPlot('grid', grid);
    const solarp = JSON.parse(data.solarp);
    Plotly.newPlot('solarp', solarp);
});