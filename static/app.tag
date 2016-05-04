<app>
  <div class="navbar-fixed">
    <nav class="teal accent-4 ">
    <div class="container">
      <div class="nav-wrapper">
        <a href="/" class="brand-logo">{ opts.title }</a>
        <ul class="right hide-on-med-and-down">
          <li><a href="/">登录</a></li>
          <li><a href="/">注册</a></li>
        </ul>
      </div>
    </div>
    </nav>
  </div>
<!-- layout -->
  <div class="container">
    <ul class="collection">
        <li each={ items } class="collection-item">
            <a href="{ link }"> <span class="title">{ title } </span></a>
        </li>
    </ul>
  </div>
  <footer class="page-footer teal accent-4">
          <div class="container">
            <div class="row">
              <div class="col l6 s12">
                <h5 class="white-text">敬请期待</h5>
                <p class="grey-text text-lighten-4">You can use rows and columns here to organize your footer content.</p>
              </div>
              <div class="col l4 offset-l2 s12">
                <h5 class="white-text">GitHub</h5>
                <ul>
                  <li><a class="grey-text text-lighten-3" href="https://github.com/rainyear">Author</a></li>
                </ul>
              </div>
            </div>
          </div>
          <div class="footer-copyright">
            <div class="container">
            © 2016 Copyright PyHub
            </div>
          </div>
        </footer>

  // logic comes here
  this.items = opts.links
</app>
