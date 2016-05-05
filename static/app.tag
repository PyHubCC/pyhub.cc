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
                    <a class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect">
                        <i class="material-icons">favorite_border</i>
                    </a>
                    <a class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect">
                      { via }
                    </a>
                </div>
            </div>
        </ul>

        </div>
    </div>
    <div class="mdl-cell mdl-cell--4-col"></div>
</div>

<footer class="mdl-mini-footer">
  <div class="mdl-mini-footer__left-section">
    <div class="mdl-logo">© pyhub.cc 2016</div>
  </div>
</footer>
  // logic comes here
  this.items = opts.links
</app>
