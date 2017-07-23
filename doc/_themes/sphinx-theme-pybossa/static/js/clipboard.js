var client = new ZeroClipboard( document.getElementsByClassName("copy-button"), {
  moviePath: "/assets/ZeroClipboard.swf"
} );

client.on( "load", function(client) {
  //alert( "movie is loaded" );

  client.on( "complete", function(client, args) {
    //console.log(args.text);
  } );
} );
