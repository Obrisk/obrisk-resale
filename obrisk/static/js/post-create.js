var toolbarOptions = {
  container: [
    [{
      'header': [1, 2, 3, 4, 5, 6, false]
    }],
    ['bold', 'italic', 'underline', 'strike'], // toggled buttons
    ['blockquote', 'code-block'],

    [{
      'list': 'ordered'
    }, {
      'list': 'bullet'
    }],

    [{
      'indent': '-1'
    }, {
      'indent': '+1'
    }], // outdent/indent
    [{
      'color': []
    }], // dropdown with defaults from theme

    [{
      'align': []
    }],
    ['link', 'image']

  ], handlers: {
    'emoji': function () { }
  }
}

Quill.register('modules/blotFormatter', QuillBlotFormatter.default);

  var quill = new Quill('#editor', {
    modules: {
      //toolbar: toolbarOptions,
      "emoji-toolbar": true,
      "emoji-shortname": true,
      "emoji-textarea": true,
      magicUrl: true,
      blotFormatter: {}
    },
    placeholder: 'Compose an epic...',
    theme: 'snow',

  });


if ( typeof quill !== 'undefined' ) {
    quill.setContents("{{ form.data.content_json }}")
    quill.on('text-change', function (delta, oldDelta, source) {
      $("#id_content").val(quill.getContents());
    });

 } else {
    $.wnoty({
        type: "error",
        autohide: false,
        message:
        "Sorry! The editor isn't working. Please try again later!"
    });
}
