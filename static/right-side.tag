<right-side>
  <!-- wechat box -->
  <div class="page-content mdl-list mdl-cell--10-col mdl-cell--8-col-phone card-join-pyhub-wrap">
    <div class="card-join-pyhub mdl-card mdl-cell--12-col-phone">
    </div>
  </div>
  <!-- end wechat box -->
  <div class="page-content mdl-list mdl-cell--10-col mdl-cell--12-col-phone card-join-pyhub-wrap">
    <div class="demo-card-square mdl-card mdl-shadow--2dp mdl-cell--12-col-phone">
      <div class="mdl-card__title">
        <h2 class="mdl-card__title-text"><i class="material-icons">chat</i>  留言框</h2>
      </div>
      <div class="mdl-card__actions mdl-card--border">
        <div class="mdl-card__supporting-text msg-spinner-container" hide={ msg_loaded }>
          <div class="mdl-spinner mdl-js-spinner is-active"></div>
        </div>
        <ul class="msg-list mdl-list" show={ msg_loaded }>
          <li class="mdl-list__item mdl-list__item--three-line msg_list__item" each={ messages }>
            <span class="mdl-list__item-primary-content">
              <span>{ user }</span>
              <span class="mdl-list__item-text-body">
                { content }
              </span>
            </span>
            <span class="mdl-list__item-secondary-content">
              <span class="mdl-list__item-secondary-info">{ timestamp }</span>
            </span>
          </li>
        </ul>
        <!-- Simple Textfield -->
        <form onsubmit={ send_msg }>
          <div class="mdl-textfield mdl-js-textfield">
            <input class="mdl-textfield__input" type="text" id="msg_input" required>
            <label class="mdl-textfield__label" for="msg_input">Text...</label>
          </div>
          <button class="mdl-button mdl-js-button mdl-button--raised mdl-button--colored" disabled={ !msg_loaded || opts.uid == undefined }>
            留言
          </button>
        </form>
      </div>
    </div>
  </div>
  <!-- update info box -->
  <div class="page-content mdl-list mdl-cell--10-col mdl-cell--12-col-phone">
    <div class="demo-card-square mdl-card mdl-shadow--2dp mdl-cell--12-col-phone">
      <div class="mdl-card__title">
        <h2 class="mdl-card__title-text"><i class="material-icons">event</i> Update</h2>
      </div>
        <div class="mdl-card__actions mdl-card--border">
            <div class="mdl-card__supporting-text" each={ opts.events }>
              <i class="material-icons">done</i> {date}: { msg }
            </div>
        </div>
      </div>
    </div>
    <!-- end update info box -->
    <!-- new user box -->
    <div class="page-content mdl-list mdl-cell--10-col mdl-cell--12-col-phone">
      <div class="demo-card-square mdl-card mdl-shadow--2dp mdl-cell--12-col-phone">
        <div class="mdl-card__title">
          <h2 class="mdl-card__title-text"><i class="material-icons">account_box</i>New Pythoners</h2>
        </div>
          <div class="mdl-card__actions mdl-card--border">
              <div class="mdl-card__supporting-text" each={ opts.users }>
                <span class="devicons devicons-python pythoners"></span> <a href='https://github.com/{uid}' target='_blank'>{ nick }</a>
              </div>
          </div>
        </div>
      </div>
      <!-- end new user box -->
  </div>
  <script>
    // logic comes here
    this.messages = [];
    this.msg_loaded = false;
    this.on('mount', function () {
      var self = this;
      $.get('/api/v1/msg', {}, function (json) {
        json = JSON.parse(json);
        self.messages = json.msgs;
        self.messages;
        self.msg_loaded = true;
        self.update();
      });
    });
    this.send_msg = function (e) {
      if (opts.uid === undefined) {
        alert('请先登录！');
        return false;
      }
      var msg_content = this.msg_input.value;
      this.msg_loaded = false;
      var self = this;
      $.post('/api/v1/msg', {msg: msg_content}, function (json){
        json = JSON.parse(json);
        self.messages.reverse();
        self.messages.push(json.msg);
        self.messages.reverse();
        self.msg_input.value = '';
        self.msg_loaded = true;
        self.update();
      })
    };
  </script>
</right-side>
