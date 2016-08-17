(function($) {
  var namespace = '/socket';
  var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
  var $hour_store = $('span#hour');
  var $minute_store = $('span#minute');

  socket.on('change hour', function(msg) {
    var path = msg.img_path;
    $hour_store.children('img').attr('src', path);
  });

  socket.on('change minute', function(msg) {
    var path = msg.img_path;
    $minute_store.children('img').attr('src', path);
  });
})(jQuery);
