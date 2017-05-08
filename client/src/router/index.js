import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import sheet from '@/components/sheet'
import index from '@/components/index'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'index',
      component: index,
    },
		{
			path: '/sheet/:id',
			name: 'sheet',
			component: sheet,
		},
  ]
})
