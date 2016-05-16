<users>
  <ul class="demo-list-item mdl-list">
    <li class="mdl-list__item" each={opts.users}>
      <i class="material-icons mdl-list__item-icon">person</i>
      <span class="mdl-list__item-primary-content">
        { nick }
      </span>
    </li>
  </ul>
</users>
<links>

</links>
<topics>
  <table class="mdl-data-table mdl-js-data-table  mdl-shadow--2dp">
    <thead>
      <tr>
        <th>标题</th>
        <th>数量</th>
        <th>关注人数</th>
        <th>链接（SLUG）</th>
        <th>是否公开</th>
        <th>等级</th>
        <th>操作</th>
      </tr>
    </thead>
    <tbody>
      <tr each={topic_metas}>
        <td>{title}</td>
        <td>{count}</td>
        <td>{favs}</td>
        <td>{slug}</td>
        <td>
          <label class="mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect" for="{_id}-is-public">
            <input type="checkbox" id="{_id}-is-public" class="mdl-checkbox__input" checked={public}>
          </label>
        </td>
        <td>{rank}</td>
        <td>
          <button class="mdl-button mdl-js-button mdl-button--raised">
            提交
          </button>
        </td>
      </tr>
    </tbody>
  </table>
  <hr/>
  <h4>添加专题</h4>
  <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
    <input class="mdl-textfield__input" type="text" id="title">
    <label class="mdl-textfield__label" for="sample3">标题</label>
  </div>
  <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
    <input class="mdl-textfield__input" type="text" id="slug">
    <label class="mdl-textfield__label" for="sample3">链接</label>
  </div>
  <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
    <input class="mdl-textfield__input" type="text" id="rank">
    <label class="mdl-textfield__label" for="sample3">等级</label>
  </div>
  <label class="mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect" for="checkbox-1">
    <input type="checkbox" id="public" class="mdl-checkbox__input" checked>
    <span class="mdl-checkbox__label">公开</span>
  </label>
  <button class="mdl-button mdl-js-button mdl-button--raised mdl-button--colored" onclick={add_topic}>
    添加
  </button>

  <script>
    this.topic_metas = opts.topic_metas;
    this.add_topic   = function (e) {
      var title = this.title.value,
          slug  = this.slug.value,
          rank  = parseInt(this.rank.value),
          is_public = this.public.value == "on";
      if (title.length * slug.length * rank.length == 0) {
        alert("格式不对!");
      } else {
        var data = {
          title: title,
          slug : slug,
          rank: rank,
          "public": is_public,
          favs: 0,
          count: 0,
        };
        $.post('/admin', {'act': 'create_topic', 'data': JSON.stringify(data)}, function (res) {
          console.log(res);
          // window.location = window.location.href;
        });
      }
    }
  </script>
</topics>
