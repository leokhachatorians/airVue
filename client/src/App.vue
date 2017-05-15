<template>
  <div id="app">
      <nav class="navbar navbar-static-top" role="navigation">
        <ul class="nav navbar-top-links navbar-left" style="margin-left: 20px;">
          <li>
            <router-link :to="{name: 'index'}" class="navbar-brand">Table List</router-link>
          </li>
        </ul>
        <ul class="nav navbar-top-links navbar-right">
          <li>
            <a href="#">
              <i class="fa fa-sign-out">Logout</i>
            </a>
          </li>
        </ul>
      </nav>
    <img src="./assets/logo.png">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'app'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
