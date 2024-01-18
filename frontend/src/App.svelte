<script>
  import {Router, Route, Link} from "svelte-routing"
  import Welcome from "./lib/Welcome.svelte";
  import Upload from "./lib/Upload.svelte"
</script>

<style>
</style>

<Router>
  <main>
    <Route path="/" component={Welcome} /> 
    <Route path="/upload" component={Upload} /> 
  </main>
</Router>