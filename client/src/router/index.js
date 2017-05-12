import Vue from 'vue'
import Router from 'vue-router'
import sheet from '@/components/sheet'
import index from '@/components/index'
import modify from '@/components/modify'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'index',
      component: index,
    },
		{
			path: '/sheet/:id/:name',
			name: 'sheet',
			component: sheet,
		},
		{
			path: '/sheet/modify/:id/:name',
			name: 'modify',
			component: modify,
		},
  ]
})
