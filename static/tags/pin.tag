<pin>
  <ul class="mdl-list" each={ chunks }>
      <hr show={ hr } />
      <button class="mdl-button mdl-js-button" disabled>
        <i class="material-icons">today</i> { date }
      </button>
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
                <i class="material-icons">star</i>
              </button>
            </div>
        </div>
      </li>
  </ul>
  <!-- Raised button with ripple -->
  <button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent" onclick={ load_more } id="btn_load_more" disabled={loading}>
      <i class="material-icons">access_time</i> 昨日推荐
  </button>

  <script>
    // js
    Date.prototype.fmt= function () {
      var m = this.getMonth()+1;
      m = m < 10 ? '0'+m : m;
      var d = this.getDate();
      d = d < 10 ? '0'+d : d;
      return this.getFullYear() + '-' + m + '-' + d;
    };
    this.admin = opts.admin;
    this.loading = false;
    this.current_date = new Date();
    this.chunks = [{items: opts.links, date: this.current_date.fmt(), hr: false}]
    console.log(this.chunks);
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
      self.loading = true;
      self.current_date.setDate(self.current_date.getDate() - 1);
      $.post('/more_pin/' + self.current_date.fmt(),{},function(json){
        if (self.current_date.fmt() === "2016-05-18") {
          self.loading = true;
        } else {
          self.loading = false;
        }
        self.chunks.push({items: json.links, date: self.current_date.fmt(), hr: 1});
        self.update();
      });
    }
    this.promote = function (e) {
      
    }
  </script>
</pin>
