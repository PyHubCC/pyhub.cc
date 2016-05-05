<app>
<style>
.card-wide.mdl-card {
  width: 800px;
  min-height: 60px;
}
</style>
<div class="mdl-grid">
    <div class="mdl-cell mdl-cell--4-col"></div>
    <div class="mdl-cell mdl-cell--4-col">
        <div class="page-content">
        <!-- Your content goes here -->

        <ul class="mdl-list">
            <li each={ items } class="mdl-list__item">
            <div class="card-wide mdl-card mdl-shadow--4dp">
                <div class="mdl-card__supporting-text">
                    <a href="{ link }" >{title}</a>
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
