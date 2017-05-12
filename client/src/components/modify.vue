<template>
  <div class="col-lg-12">
    <div class="ibox float-e-margins">
      <h1>Table: {{ sheet_name }}</h1> 
      <h3><button type="button" class="btn btn-xs btn-primary" style="margin-bottom: 0;"
              data-toggle="modal" data-target="#change_table_name_modal">Change Table Name</button>
      </h3>
    </div>
    <div class="ibox float-e-margins">
      <div class="ibox-title">
        <h5>Column List</h5>
        <div class="ibox-tools">
          <a class="collapse-link">
            <i class="fa fa-chevron-up"></i>
          </a>
          <a class="dropdown-toggle" data-toggle="dropdown" href="#">
            <i class="fa fa-wranch"></i>
          </a>
          <a class="close-link">
            <i class="fa fa-times"></i>
          </a>
        </div>
      </div>

    <!-- Add Column Button -->
      <div class="ibox-content">
        <div class="form-inline">
          <button v-on:click="toggle_add" type="button" class="btn btn-w-m btn-success">
            Add Column
          </button>
        </div>
      </div>
    <!-- End Add Column Button -->

    <!-- Add Column Well -->
      <div v-show="add_well" class="ibox-content col-lg-12">
        <div class="well col-lg-3">
          <form role="form" class="form-inline">
            <table class="table">
              <thead>
                <tr>
                  <th colspan="3" style="text-align: center;"><h3>Add Column</h3></th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style="vertical-align: middle;"><label class="col-lg-2 control-label">Name</label></td>
                  <td><input type="text" id="add_name" class="form-control"></td>
                </tr>
                <tr>
                  <td style="vertical-align: middle;"><label class="col-lg-2 control-label">Type</label></td>
                  <td>
                    <select id="options_add" class="form-control">
                      <option v-for="type in types" v-bind:value="type[0]">
                        {{ type[1] }}
                      </option>
                    </select>
                  </td>
                </tr>
                <tr>
                  <td></td>
                  <td class="form-inline">
                    <button v-on:click="add_column"
                      type="button" class="btn btn-s btn-primary">
                      Create
                    </button>
                    <button v-on:click="toggle_add"
                      type="button" class="btn btn-s btn-default">
                      Cancel
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </form>
        </div>
      </div>
    <!-- End of Add Column Well-->

    <!-- Edit Column Well -->
      <div v-show="edit_well" id="edit_column_well" class="ibox-content col-lg-12">
        <div class="well col-lg-6">
          <form role="form" class="form-inline">
            <table class="table">
              <thead>
                <tr>
                  <th colspan="3" style="text-align: center;"><h3 id="edit_column_header">Edit Column</h3></th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style="vertical-align: middle;"><label class="col-lg-2 control-label">Current Column Name</label></td>
                  <td><input type="text" id="old_name" class="form-control" disabled></td>
                  <td style="vertical-align: middle;"><label class="col-lg-2 control-label">New Column Name</label></td>
                  <td><input type="text" id="new_name" class="form-control"></td>
                </tr>
                <tr>
                  <td style="vertical-align: middle;"><label class="col-lg-3 control-label">Old Type</label></td>
                  <td><input type="text" id="old_type" class="form-control" disabled></td>
                  <td style="vertical-align: middle;"><label class="col-lg-2 control-label">Type</label></td>
                  <td>
                    <select id="options_edit" class="form-control">
                      <option v-for="type in types" v-bind:value="type[0]">
                        {{ type[1] }}
                      </option>
                    </select>
                  </td>
                </tr>
                <tr>
                  <td></td>
                  <td class="form-inline">
                      <button v-on:click="edit_column"
                        type="button" class="btn btn-s btn-primary">
                        Alter
                      </button>
                      <input type="hidden" id="edit_col_id" value="">
                      <button v-on:click="toggle_edit" 
                        id="cancel_edit_column_button" type="button"
                        class="btn btn-s btn-default">
                        Cancel
                      </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </form>
        </div>
      </div>
    <!-- End Edit Column Well -->

    <!-- Table of Column Info -->
      <div class="ibox-content">
        <div class="table-responsive">
          <div role="status" aria-live="polite" style="padding-bottom: 8px;">Showing 1 to 14 of 14 entries</div>
            <table class="table table-striped table-bordered table-hover dataTables-example" >
              <thead>
                <tr>
                  <th>#</th>
                  <th>Column Name</th>
                  <th>Column Type</th>
                  <th>Commands</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="column in schema">
                  <td>{{ column.num }}</td>
                  <td>{{ column.name }}</td>
                  <td>{{ column.type }}</td>
                  <td>
                    <button
                    v-on:click="toggle_edit(column.name, column.id, column.type)"
                      id="edit_column_btn"
                      type="button" class="btn btn-xs btn-success basic">
                      Edit</button>
                    <button v-on:click="delete_column(column.name, column.id)"
                      type="button" class="btn btn-xs btn-danger basic">
                      Delete
                    </button>
                    <input type="hidden" id="clicked_column_name_i.column_name" name="to_delete" value="i.column_id">
                    <input type="hidden" id="clicked_column_type_loop.index0"  value="i.column_type">
                  </td>
                </tr>
              </tbody>
            </table>
        </div> 
      </div>
    <!-- End of Table of Column Info -->
    </div>

  <!-- Change Tablename Modal -->
    <div id="change_table_name_modal" class="modal fade" role="dialog">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal">&times;</button>
            <h4 class="modal-title">Change Tablename</h4>
          </div>
          <div class="modal-body">  
            <form method="POST">
              <label class="col-lg-2 control-label">Current Tablename</label>
              <input type="text"  class="form-control" v-bind:value="sheet_name" disabled>
              </br>
              <label class="col-lg-2 control-label">New Tablename</label>
              <input type="text" id="new_sheet_name" class="form-control">
              <div class="modal-footer">
                <button v-on:click="edit_sheet_name" type="button"
                  class="btn btn-primary" data-dismiss="modal">
                  Save
                </button>
                <button type="button" 
                  class="btn btn-default" data-dismiss="modal">
                  Close
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  <!-- End Change Tablename Modal -->
  </div>
</template>

<script>
export default {
  name: 'modify',
  data () {
    return {
      sheet_name: "",
      sheet_id: parseInt(this.$route.params.id),
      user_id: 1, // hard coding atm
      schema: [],
      add_well: false,
      edit_well: false,
      types: [
        ['String', 'Text'], ['Text', 'Long Text'],
        ['Text', 'Select'], ['Boolean', 'Check Box'],
        ['Date', 'Date'], ['Text', 'Record'],
        ['Float', 'Currency'], ['Float', 'Number'],
        ['DateTime', 'Timestamp'], ['BigInteger', 'Integer'],
        ['String', 'Time']
      ]
    }
  },
  methods: {
    populate: function() {
      var self = this;
      var data = {'id': this.sheet_id};
      var url = 'http://localhost:5000/api/v1/sheet/' + this.sheet_id;
      axios.get(url)
      .then(response => {
        self.sheet_name = response.data['sheet_name'];
        self.schema = response.data['schema'];
      })
      .catch(function (err) {
        console.log(err.message);
      })
    },
    delete_column: function(column_name, column_id) {
      var self = this;
      var data = {
        'column_name': column_name,
        'column_id': column_id,
        'sheet_id': this.sheet_id,
      };
      var url = 'http://localhost:5000/api/v1/sheet/' + this.sheet_id + '/columns/' + column_id;
      axios.delete(url, data)
      .then(response => {
        self.populate();
      })
      .catch(function (err) {
        console.log(err.message);
      });
    },
    toggle_edit: function(column_name=false, column_id=false, column_type=false) {
      if (column_id != false) { 
        document.getElementById('old_name').value = column_name;
        document.getElementById('old_type').value = column_type;
        document.getElementById('edit_col_id').value = column_id;
        this.edit_well = true;
      }
      else {
        this.edit_well = !this.edit_well;
      }
    },
    toggle_add: function() {
      document.getElementById('add_name').value = "";
      this.add_well = !this.add_well;
    },
    edit_column: function() {
      var e = document.getElementById('options_edit');
      var new_name = document.getElementById('new_name').value;
      var old_name = document.getElementById('old_name').value;
      var new_type = e.options[e.selectedIndex].value;
      var col_id = document.getElementById('edit_col_id').value;
      var data = {
        'sheet_id': this.sheet_id,
        'old_name': old_name,
        'new_name': new_name,
        'new_type': new_type,
        'col_id': col_id,
      };
      var self = this;
      var url = 'http://localhost:5000/api/v1/sheet/' + this.sheet_id + '/columns/' + col_id;
      axios.put(url, data)
      .then(function (res) {
        self.toggle_edit();
        self.populate();
      })
      .catch(function (err) {
        console.log(err.message);
      });
    },
    add_column: function() {
      var e = document.getElementById('options_add');
      var col_type = e.options[e.selectedIndex].value;
      var col_name = document.getElementById('add_name').value;
      var data = {
        'sheet_id': this.sheet_id,
        'column_name': col_name,
        'column_type': col_type
      };
      var self = this;
      var url = 'http://localhost:5000/api/v1/sheet/' + this.sheet_id + '/columns';
      axios.post(url, data)
      .then(function (res) {
        self.toggle_add();
        self.populate();
      })
      .catch(function (err) {
        console.log(err.message);
      });
    },
    edit_sheet_name: function() {
      var new_sheet_name = document.getElementById('new_sheet_name').value;
      var data = {
        'sheet_id': this.sheet_id,
        'new_sheet_name': new_sheet_name
      };
      var self = this;
      var url = 'http://localhost:5000/api/v1/sheet/' + this.sheet_id + '/update';
      axios.post(url, data)
      .then(function (res) {
        self.populate();
      })
      .catch(function (err) {
        console.log(err.message);
      });
    },
  },
  beforeMount() {
    this.populate();
  }
}
</script>

<style>
.basic {
  margin-bottom: 0;
}
</style>
