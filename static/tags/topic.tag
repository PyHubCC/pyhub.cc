<topic>
  <div class="mdl-grid">
    <div class="mdl-cell mdl-cell--4-col mdl-card mdl-shadow--2dp topic-cell" each={ opts.topic_meta} style="background-image: {gen_geo(title, rank)}" onclick={goto}>
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
    .topic-cell {cursor: pointer;}
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
    this.gen_geo = function (title, rank) {
      var self = this;
      function getRandomArbitrary(min, max) {
        return Math.floor(Math.random() * (max - min) + min);
      }
      return this.GP.generate(title, {
        // generator: self.PATTERNS[getRandomArbitrary(0, self.PATTERNS.length)],
        generator: self.PATTERNS[rank],
      }).toDataUrl();
    };
    this.goto = function (e) {
      /*
      var slug = e.item.slug;
      console.log(slug);
      window.location = '/topic/'+slug;
      */
      window.toast("模块正在开发中，敬请期待！");
    };

  </script>
</topic>
