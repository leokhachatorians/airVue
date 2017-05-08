<template>
  <div class="col-lg-12">
    <div class="ibox float-e-margins">

      <!-- Top Section -->
      <div class="ibox-title">
        <h5>Your Tables</h5>
      </div>

      <div class="ibox-content">
	      <button id="new_table_button" type="button" class="btn btn-w-m btn-success" style="margin-bottom: 0;">Create New Table</button>
      </div>
      <!-- End Top Section -->

      <!-- Create Table Well -->
      <div id="create_table_well" class="ibox-content col-lg-12" style="display: none;">
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
                    <td></td>
                    <td class="form-inline">
                      <button type="button" id="cancel_new_table_button" class="btn btn-s btn-default" style="margin-bottom: 0; margin-left: 10px">Cancel</button>
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
          <div role="status" aria-live="polite" style="padding-bottom: 8px;">
            Showing 1 to 14 of 14 entries
          </div>

          <!-- View Table List Section -->
          <table class="table table-striped table-bordered table-hover dataTables-Example">
            <thead>
              <tr>
                <th>Table Name</th>
                <th>Commands</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="form-inline">
                  <form method="POST">
                  </form>
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
    name: 'hello',
    data () {
      return {
        msg: 'Welcome to Your Vue.js App'
      }
    }
  }
</script>
