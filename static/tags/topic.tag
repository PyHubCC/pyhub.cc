<topic>
  <style>
  .demo-card-wide.mdl-card {
  width: 512px;
  }
  .demo-card-wide > .mdl-card__title {
  color: #fff;
  height: 176px;
  background: url('/static/welcome_card.jpg') center / cover;
  }
  .demo-card-wide > .mdl-card__menu {
  color: #fff;
  }
  </style>
    <div class="demo-card-wide mdl-card mdl-shadow--2dp" show={ false }>
    <div class="mdl-card__title">
      <h2 class="mdl-card__title-text">Coming soon!</h2>
    </div>
    <div class="mdl-card__supporting-text">
      去为你感兴趣的 Python 专题投票！
    </div>
    <div class="mdl-card__actions mdl-card--border">
      <a class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect"
        target="_blank"
        href="http://mp.weixin.qq.com/s?__biz=MzI0NjIxMzE5OQ==&mid=2656697793&idx=1&sn=9a01de43e5c0a64f702887176e909142#rd">
        马上去投票
      </a>
    </div>
  </div>

  <div class="mdl-grid">
    <div class="mdl-cell mdl-cell--4-col mdl-card mdl-shadow--2dp" each={ opts.topic_meta} style="background-image: {gen_geo(title)}" >
      <div class="mdl-card__title mdl-card--expand" >
        <h4>{ title }</h4>
      </div>
      <div class="mdl-card__actions mdl-card--border topic-meta-info">
        <i class="material-icons">extension</i><span>{ count }</span>
        <i class="material-icons">remove_red_eye</i><span>{ favs }</span>
      </div>
    </div>
  </div>
  <style>
    .mdl-card__title h4 {color:#fff; font-weight: 800; text-shadow: 0 3px 0 rgba(0, 0, 0, .15)}
    .topic-meta-info {padding-left: 14px;}
    .topic-meta-info i{color: #eee; font-size: 16px; vertical-align:middle; margin-left: 2px;}
    .topic-meta-info span {color: #eee; font-size: 12px; vertical-align:middle; margin-left: 2px;}
  </style>

  <script>
    this.GP = opts.GP;
    this.PATTERNS = [
    	'octogons',
    	'overlappingCircles',
    	'plusSigns',
    	'xes',
    	'sineWaves',
    	'hexagons',
    	'overlappingRings',
    	'plaid',
    	'triangles',
    	'squares',
    	'concentricCircles',
    	'diamonds',
    	'tessellation',
    	'nestedSquares',
    	'mosaicSquares',
    	'chevrons'
    ];
    this.gen_geo = function (title) {
      var self = this;
      function getRandomArbitrary(min, max) {
        return Math.floor(Math.random() * (max - min) + min);
      }
      return this.GP.generate(title, {
        generator: self.PATTERNS[getRandomArbitrary(0, self.PATTERNS.length)],
      }).toDataUrl();
    }

  </script>
</topic>
