<template>
  <div class="col-lg-12">
    <div class="ibox float-e-margins">

    <!-- Top Section -->
      <div class="ibox-title">
        <h5>Your Tables</h5>
      </div>

      <div class="ibox-content">
	      <button v-on:click="toggle_well()" id="new_table_button" 
          type="button" class="btn btn-w-m btn-success basic">
          Create New Table
        </button>
      </div>
    <!-- End Top Section -->

    <!-- Create Table Well -->
      <div v-show="display_well" class="ibox-content col-lg-12">
        <div class="well col-lg-3">
          <form role="form" method="POST" class="form-inline">
              <table class="table">
                <thead>
                  <tr>
                    <th colspan="3" style="text-align: center;"><h3>New Table</h3></th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style="vertical-align: middle;"><label class="col-lg-2 control-label">Table</label></td>
                    <td><input type="text" placeholder="My Table" class="form-control" id="sheet_name_input"></td>
                  </tr>
                  <tr>
                    <td></td>
                    <td>
                      <button v-on:click="create_sheet" type="button"
                        class="btn btn-s btn-primary basic">Create</button>
                      <button v-on:click="toggle_well" 
                        type="button" class="btn btn-s btn-default left">Cancel</button>
                    </td>
                  </tr>
              </tbody>
              </table>
            </form>
        </div>
      </div>
    <!-- End Create Table Well -->

    <!-- Contents -->
      <div class="ibox-content">
        <div class="table-responsive">
        <!-- View Table List Section -->
          <table class="table table-striped table-bordered table-hover dataTables-Example">
            <thead>
              <tr>
                <th>Table Name</th>
                <th>Commands</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="sheet in sheets">
                <td>
                  <router-link :to="{name: 'sheet', params: {id: sheet.id, name: sheet.name}}">{{ sheet.name }}</router-link>
                <td class="form-inline">
                  <button v-on:click="delete_sheet(sheet.id)"
                    class="btn btn-xs btn-danger basic" type="button">Delete</button>
                  <router-link :to="{name: 'modify', params: {id: sheet.id, name: sheet.name}}">
                    <button class="btn btn-xs btn-success basic" type="button">Edit Table</button>
                  </router-link>
                  <input type="hidden" v-bind:value="sheet.id" id="table_id">
                </td>
              </tr>
            </tbody>
          </table>
        <!-- End View Table List Section -->
        </div>
      </div>
    <!-- End Contents -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'index',
  data () {
    return {
      sheets: [],
      display_well: false,
      user_id: 1,
    }
  },
  methods: {
    populate: function() {
      var url = 'http://localhost:5000/api/v1/user/' + this.user_id + '/sheets';
      axios.get(url)
      .then(response => {
        this.sheets = response.data['sheets'];
      })
      .catch(function (err) {
        console.log(err.message);
      });
    },
    toggle_well: function() {
      this.display_well = !this.display_well;
      document.getElementById('sheet_name_input').value = "";
    },
    create_sheet: function() {
      var sheet_name = document.getElementById('sheet_name_input').value;
      var data = {'sheet_name': sheet_name};
      var url = 'http://localhost:5000/api/v1/user/' + this.user_id + '/sheets';
      axios.post(url, data)
      .then(response => {
        this.populate()
        this.toggle_well()
      })
      .catch(function (err) {
        console.log(err.message);
      });
    },
    delete_sheet: function(id) {
      var url = 'http://localhost:5000/api/v1/user/' + this.user_id + '/sheets/' + id;
      axios.delete(url)
      .then(response => {
        this.populate()
      })
      .catch(function (err) {
        console.log(err.message);
      });
    }
  },
  created() {
    this.populate()
  },
}
</script>

<style>
.basic {
  margin-bottom: 0;
}

.left {
  margin-bottom: 0;
  margin-left: 10px;
}

.center-block {
  display: block;
  margin-right: auto;
  margin-left: auto;
  text-align: center;
}
</style>
