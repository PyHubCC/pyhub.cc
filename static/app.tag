<app>
<div class="mdl-grid">
    <div class="mdl-cell mdl-cell--2-col"></div>
    <div class="mdl-cell mdl-cell--6-col mdl-cell--8-col-tablet mdl-cell--12-col-phone">
      <div class="page-content">
        <!-- Your content goes here -->
        <ul class="mdl-list">
            <li each={ items } class="mdl-list__item">
            <div class="card-wide mdl-card mdl-shadow--4dp mdl-cell--12-col">
                <div class="mdl-card__supporting-text">
                    <a href="{ link }" target="_blank"><h6>{title} <br/><span class="link-host"> { host }</h6></a>
                    <p>
                        {abstract}
                    </p>
                </div>
                <div class="mdl-card__actions mdl-card--border">
                    <a class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect" link-id={ _id } onclick={ vote }>
                        <i class="material-icons">{ is_faved() }</i> { favs }
                    </a>
                    <a class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect">
                      { via }
                    </a>
                    <a class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect" show={ admin } onclick={ unpublic }>
                      <i class="material-icons" >delete_forever</i>
                    </a>
                </div>
            </div>
            </li>
        </ul>
        <!-- Raised button with ripple -->
        <button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent" onclick={ load_more } id="btn_load_more">
            加载更多
        </button>
      </div>
    </div>
    <div class="mdl-cell mdl-cell--4-col">
      <!-- wechat box -->
      <div class="page-content mdl-list mdl-cell--10-col card-join-pyhub-wrap">
        <div class="card-join-pyhub mdl-card">
        </div>
      </div>
      <!-- end wechat box -->
      <div class="page-content mdl-list mdl-cell--10-col card-join-pyhub-wrap">
        <div class="demo-card-square mdl-card mdl-shadow--2dp">
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
      <div class="page-content mdl-list mdl-cell--10-col">
        <div class="demo-card-square mdl-card mdl-shadow--2dp">
          <div class="mdl-card__title">
            <h2 class="mdl-card__title-text"><i class="material-icons">event</i> Update</h2>
          </div>
            <div class="mdl-card__actions mdl-card--border">
              <div class="mdl-card__menu">
                <button class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect">
                  <i class="material-icons">share</i>
                </button>
              </div>
                <div class="mdl-card__supporting-text" each={ opts.events }>
                  <i class="material-icons">done</i> {date}: { msg }
                </div>
            </div>
          </div>
        </div>
        <!-- end update info box -->
        <!-- new user box -->
        <div class="page-content mdl-list mdl-cell--10-col">
          <div class="demo-card-square mdl-card mdl-shadow--2dp">
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
    </div>
</div>

<footer class="mdl-mini-footer">
  <div class="mdl-mini-footer__left-section">
    <ul class="mdl-mini-footer__link-list">
      <li>
        <a href='https://pyhub.cc'><i class="devicons devicons-python" />PyHub.cc</a>
      </li>
      <li>
        <a href="https://github.com/PyHubCC"><i class="devicons devicons-github_badge" />GitHub</a></li>
      <li>
        <a href="http://rainy.im/donate" target="_blank">
          <i class="devicons devicons-coffeescript" />Donate</a>
      </li>
    </ul>
  </div>
</footer>
<script>
  // logic comes here
  this.messages = [];
  this.msg_loaded = false;
  this.admin = opts.admin;
  this.page_no = opts.page_no;
  this.items = opts.links;
  this.loading = false;
  this.on('mount', function () {
    var self = this;
    $.get('/api/v1/msg', {}, function (json) {
      json = JSON.parse(json);
      self.messages = json.msgs;
      self.messages.reverse();
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
      self.messages.push(json.msg);
      self.msg_input.value = '';
      self.msg_loaded = true;
      self.update();
    })
  };

  this.vote = function(e){
    if (opts.uid === undefined) {
      alert('请先登录！');
      return;
    }
    e.preventUpdate = true; // Why this???
    var self = this;
    var link_id = self._id;
    var favlist = self.favlist;
    if (favlist != undefined && favlist.indexOf(opts.uid) >= 0) {
      alert('已收藏！');
      self.update();
    } else {
      $.post('/act/'+link_id, {'action': 'FAV'}, function(json){
        if (favlist === undefined) {
          self.favlist = [opts.uid];
        } else {
          self.favlist.push(opts.uid);
        }
        self.favs += 1;
        self.update();
      })
    };
  }
  this.is_faved = function() {
    return this.favlist === undefined || this.favlist.indexOf(opts.uid) == -1 ? 'favorite_border' : 'favorite';
  }
  this.load_more = function(e){
    var self = this;
    this.page_no += 1;
    $.post('/share/' + this.page_no,{},function(json){
      var data = JSON.parse(json);
      for (record of data){
        self.items.push(record);
      }
      self.update();
    })
  }
  this.unpublic = function(e) {
    var self = this;
    if(confirm('DELETE '+ this.title +'?')){
        var index = self.items.indexOf(e.item);
        self.items.splice(index, 1);
      $.post('/act/'+self._id, {'action': 'DEL'}, function(json){
      })
    }
  }
</script>
</app>
