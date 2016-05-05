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
                    <a href="{ link }" ><h6>{title}</h6></a>
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
                </div>
            </div>
            </li>
        </ul>
        <!-- Raised button with ripple -->
        <button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent" onclick={ load_more }>
            加载更多
        </button>
      </div>
    </div>
    <div class="mdl-cell mdl-cell--4-col">
      <div class="page-content mdl-list">
        <img src="/static/join.png" class="mdl-cell mdl-cell--10-col"/>
      </div>
    </div>
</div>

<footer class="mdl-mini-footer">
  <div class="mdl-mini-footer__left-section">
    <div class="mdl-logo">PyHub.cc</div>
    <ul class="mdl-mini-footer__link-list">
      <li><a href="#">Help</a></li>
      <li><a href="#">Privacy & Terms</a></li>
    </ul>
  </div>
</footer>
  // logic comes here
  this.page_no = opts.page_no;
  this.items = opts.links;
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
  this.vote = function(){
    if (opts.uid === undefined) {
      alert('请先登录！');
    }
    var self = this;
    var link_id = this._id;
    var favlist = this.favlist;
    if (favlist != undefined && favlist.indexOf(opts.uid) >= 0) {
      alert('已收藏！')
    } else {
      $.post('/fav/'+link_id, {}, function(json){
        if (favlist === undefined) {
          self.favlist = [opts.uid];
        } else {
          self.favlist.push(opts.uid);
        }
        self.update();
      })
    }
  }
  this.is_faved = function() {
    return this.favlist === undefined || this.favlist.indexOf(opts.uid) == -1 ? 'favorite_border' : 'favorite';
  }
</app>
