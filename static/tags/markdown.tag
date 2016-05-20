<markdown>
  <div id="editormd">
      <textarea style="display:none;">### Hello Editor.md !</textarea>
  </div>

  <script>
    this.on('mount', function () {
      opts.editormd("editormd", {
          path : "../lib/" // Autoload modules mode, codemirror, marked... dependents libs path
        });
    });
  </script>
</markdown>
