<template>
  <div class="col-lg-12">
    <div class="ibox float-e-margins">
      <h1>Table: {{ sheet_name }}</h1>
    </div>

    <div v-if="allow_data" class="ibox float-e-margins">
      <input v-for="column in inputs" v-bind:placeholder="column" name="add_records" type="text">
      <button v-on:click="add_data" type="button" class="btn btn-s btn-primary">Add</button>

      <div class="ibox-content">
        <div class="table-responsive">
          <table class="table table-striped table-bordered table-hover dataTables-example">
            <thead> 
              <tr>
                <th width="5" style="border-right-style: hidden;"></th>
                <th v-for="column in columns" class="column">{{ column }}</th>
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
                    <button v-on:click="delete_data" type="button" 
                      class="btn btn-xs btn-danger">X</button>
                    <button v-on:click="edit_data" type="button" 
                      class="btn btn-xs btn-success">Save</button>
                  </form>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <div v-else>
      <h1>You have no columns! Click 
        <router-link :to="{name: 'modify', params: {id: sheet_id, name: sheet_name}}">here</router-link>
        to create some</h1>
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
      allow_data: false,
      sheet_name: this.$route.params.name,
      sheet_id: parseInt(this.$route.params.id),
    }
  },
  methods: {
    populate: function() {
      var d = {'id': this.sheet_id};
      var url = 'http://localhost:5000/api/v1/sheet/' + this.sheet_id + '/contents';
      axios.get(url)
      .then(response => {
        this.my_list = response.data['cells'];
        this.columns = response.data['columns'];
        this.inputs = response.data['inputs'];
        this.allow_data = this.inputs.length > 0 ? true : false;
      })
      .catch(function (err) {
        console.log(err.message);
      });
    },
    add_data: function() {
      var add_records = document.getElementsByName('add_records');
      var data = {}
      data['values'] = []
      for (var i = 0; i < add_records.length; i++) {
        data['values'].push(add_records[i]['value'])
      }
      var url = 'http://localhost:5000/api/v1/sheet/' + this.sheet_id + '/entry';
      axios.post(url, data)
      .then(response => {
        this.clear_inputs();
        this.populate();
      })
      .catch(function (err) {
        console.log(err.message);
      });
    },
    delete_data: function(e) {
      var form = e.target.form;
      var row_id = form.elements.namedItem('row_id').value;
      var url = 'http://localhost:5000/api/v1/sheet/' + this.sheet_id + '/entry/' + row_id;
      axios.delete(url)
      .then(response  => {
        this.populate();
      })
      .catch(function (err) {
        console.log(err.message);
      });
    },
    edit_data: function(e) {
      var form = e.target.form;
      var row_id = form.elements.namedItem('row_id').value;
      var data = {}
      data['values'] = []
      var input_nodes = document.getElementsByName(row_id);
      for (var i = 0; i < input_nodes.length; i++) {
        data['values'].push(input_nodes[i].value);
      }
      var url = 'http://localhost:5000/api/v1/sheet/' + this.sheet_id + '/entry/' + row_id;
      axios.put(url, data)
      .then(response => {
        this.populate()
      })
      .catch(function (err) {
        console.log(err.message);
      });
    },
    clear_inputs: function(e) {
      var inputs = document.getElementsByName('add_records');
      for (var i = 0; i < inputs.length; i++) {
        inputs[i].value = "";
      }
    }
  },
  beforeMount() {
    this.populate()
  },
}
</script>

<style>
.column {
  text-align: center;
}
</style>
