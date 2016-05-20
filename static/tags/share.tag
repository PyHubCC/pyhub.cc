<share>
  <ul class="mdl-list" >
      <li each={ items } class="mdl-list__item">
        <div class="card-wide mdl-card mdl-shadow--4dp mdl-cell--12-col">
            <div class="mdl-card__supporting-text">
                <a href="{ link }" target="_blank"><h6>{title} <br/><span class="link-host"> { host } via {via} </span> </h6></a>
                  <p>
                      {abstract}
                  </p>
            </div>
            <div class="mdl-card__actions mdl-card--border mdl-grid">
              <div class="mdl-grid action-btns">
                <div class="mdl-cell mdl-cell--3-col mdl-cell--1-col-phone mdl-cell--3-col-tablet">
                  <a class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect" link-id={ _id } onclick={ vote }>
                      <i class="material-icons">{ is_faved() }</i> { favs }
                  </a>
                </div>
                <div class="mdl-cell mdl-cell--3-col mdl-cell--1-col-phone mdl-cell--3-col-tablet">
                  <a class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect" href="/py/{ _id }">
                    <i class="material-icons">share</i>
                  </a>
                </div>
                <div class="mdl-cell mdl-cell--3-col mdl-cell--1-col-phone mdl-cell--3-col-tablet">
                  <a class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect" href="/py/{ _id }">
                    <i class="material-icons">textsms</i> { comments || 0 }
                  </a>
                </div>
                <div class="mdl-cell mdl-cell--3-col mdl-cell--hide-phone mdl-cell--3-col-tablet">
                  <a class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect" href="/u/{via_uid}">
                    <img src="{via_avatar} " class="avatar-square"/>
                  </a>
                </div>
              </div>
            </div>

            <div class="mdl-card__menu" show={ admin }>
              <button class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect" onclick={ promote }>
                <i class="material-icons">{ is_promoted() }</i>
              </button>
              <button class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect" onclick={ unpublic }>
                <i class="material-icons">delete</i>
              </button>
            </div>
        </div>
      </li>
  </ul>
  <!-- Raised button with ripple -->
  <button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent" onclick={ load_more } id="btn_load_more">
      加载更多
  </button>
  <script>
  this.admin = opts.admin;
  this.page_no = opts.page_no;
  this.items = opts.links;
  this.loading = false;
  this.vote = function(e){
    if (opts.uid === undefined) {
      toast();
      return;
    }
    e.preventUpdate = true; // Why this???
    var self = this;
    var link_id = self._id;
    var favlist = self.favlist;
    if (favlist != undefined && favlist.indexOf(opts.uid) >= 0) {
      toast('已收藏！');
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
  this.is_promoted = function () {
    return this.promoted === undefined || !this.promoted ? 'star_border' : 'star';
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
  this.promote = function (e) {
    var self = this;
    if (this.promoted) {
      toast('已推荐！');
      return;
    }
    e.preventUpdate = true;
    if (confirm('推荐 《'+ this.title +'》 ？')) {
      $.post('/act/'+self._id, {'action': 'PRO'}, function (json) {
        self.promoted = true;
        self.update();
      })
    }
  }
  </script>
</share>
