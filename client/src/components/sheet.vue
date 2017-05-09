<template>
  <div class="col-lg-12">
    <div class="ibox float-e-margins">
      <form method="post" id="add_form">
        <input v-for="column in inputs" v-bind:placeholder="column" name="add_records" type="text">
        <button v-on:click="add_data" type="button" class="btn btn-s btn-primary">Add</button>
        <input type="hidden" :value="sheet_id" id="sheet_id">
      </form>

      <div class="ibox-content">
        <div class="table-responsive">
          <div role="status" aria-live="polite" style="padding-bottom: 8px;">Showing 1 to 14 of 14 Entries</div>
          <table class="table table-striped table-bordered table-hover dataTables-example">
            <thead>
              <tr>
                <th width="5" style="border-right-style: hidden;"></th>
                <th v-for="column in columns">{{ column }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="key in my_list">
                <td style="border-right-style: hidden;"></td>
                <td v-for="cell in key.cells">
                  <input type="text" v-bind:value="cell" v-bind:name="key.id">
                </td>
                <td>
                  <form method="post">
                    <input type="hidden" v-bind:value="key.id" id="row_id">
                    <button v-on:click="delete_data" type="button" class="btn btn-xs btn-danger"
                            style="margin-bottom: 0;">X</button>
                    <button v-on:click="edit_data" type="button" class="btn btn-xs btn-success"
                            style="margin-bottom: 0;">Save</button>
                  </form>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'view_sheet',
  data () {
    return {
      my_list: [],
      columns: [],
      inputs: [],
      sheet_name: '',
      sheet_id: '',
    }
  },
  methods: {
    populate_table: function() {
      var self = this;
      let id = parseInt(this.$route.params.id);
      var d = {'id': id};
      axios.post('http://localhost:5000/get_sheet', d)
        .then(response => {
              self.my_list = response.data['rows'];
              self.columns = response.data['columns'];
              self.inputs = response.data['columns'].slice(0);
              self.inputs.pop();
              self.sheet_name = response.data['sheet_info']['name'];
              self.sheet_id = response.data['sheet_info']['id'];
        })
        .catch(function (err) {
          console.log(err.message);
        });
    },
    add_data: function() {
      var self = this;
      var add_records = document.getElementsByName('add_records');
      var data = {}

      data['values'] = []
      for (var i = 0; i < add_records.length; i++) {
        data['values'].push(add_records[i]['value'])
      }
      data['sheet_id'] = document.getElementById('sheet_id').value;
      axios.post('http://localhost:5000/add_data', data)
      .then(function (res) {
          self.populate_table();
        })
        .catch(function (err) {
          console.log(err.message);
      });
    },
    delete_data: function(e) {
      var self = this;
      var form = e.target.form;
      var data = {}
      data['sheet_id'] = document.getElementById('sheet_id').value;
      data['row_id'] = form.elements.namedItem('row_id').value;
      axios.post('http://localhost:5000/delete_data', data)
        .then(function (res) {
          self.populate_table();
        })
        .catch(function (err) {
          console.log(err.message);
        });
    },
    edit_data: function(e) {
      var self = this;
      var form = e.target.form;
      var data = {}
      data['sheet_id'] = document.getElementById('sheet_id').value;
      data['row_id'] = form.elements.namedItem('row_id').value;
      data['values'] = []
      var input_nodes = document.getElementsByName(data['row_id']);
      for (var i = 0; i < input_nodes.length; i++) {
        data['values'].push(input_nodes[i].value);
      }
      axios.post('http://localhost:5000/modify_data', data)
        .then(function (res) {
          self.populate_table()
        })
      .catch(function (err) {
        console.log(err.message);
      });
    },
  },
  beforeMount() {
    this.populate_table()
  },
}
</script>
