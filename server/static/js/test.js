Vue.component('manage-posts', {
  template: '#manage-template',
  data: function() {
    return {
      posts: [
        'Vue.js: The Basics',
        'Vue.js Components',
        'Server Side Rendering with Vue',
        'Vue + Firebase'
      ]
    }
  }
})
var table = new Vue({
	el: '#current-view',
	data: {
		my_list: [],
		columns: [],
		inputs: [],
		sheet_name: "",
		sheet_id: "",
		currentView: 'manage-posts',

	},
	methods: {
		populate_table: function() {
			var self = this;
			axios.get('/get_sheet')
				.then(response => {
							self.my_list = response.data['rows'];
							self.columns = response.data['columns'];
							self.inputs = response.data['columns'];
							self.inputs.pop();
							self.sheet_name = response.data['sheet_info']['name'];
							self.sheet_id = response.data['sheet_info']['id'];
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
			axios.post('/add_data', data)
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
			axios.post('/delete_data', data)
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
			// A little hacky, but due to inability to have forms in tables,
			// have to access the input fields via their parent TD via ID (which is acutally the rowID)
			input_td_nodes = document.getElementsByName(data['row_id']);
			for (var i = 0; i < input_td_nodes.length; i++) {
				data['values'].push(input_td_nodes[i].childNodes[0].value);
			}
			axios.post('/modify_data', data)
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
})

Vue.component('column-headers', {
	props: ['column'],
	template: '<th>{{ column }}</th>'
})

Vue.component('table-cell', {
	props: ['data'],
	template: `
		<td>
			<input v-bind:value="data" id="row_cell">
		</td>
		`,
})

Vue.component('row-id', {
	props: ['data'],
	template: `<input type="hidden" v-bind:value="data.id" id="row_id">`
})

Vue.component('add-cell', {
	props: ['data'],
	template: `<input type="text" name="add_records" v-bind:placeholder='data' value="">`
})

Vue.component('create-post', {
	template:'#create-template'
})


