import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/* Router Modules */

/**
 * Note: sub-menu only app                                                                                                             ear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    noCache: true                if set true, the page will no be cached(default is false)
    affix: true                  if set true, the tag will affix in the tags-view
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: '首页',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '首页', icon: 'dashboard' }
    }]
  },

  {
    path: '/analysis',
    component: Layout,
    redirect: '/analysis/source',
    name: 'analysis',
    meta: { title: '分析', icon: 'el-icon-s-help' },
    children: [
      {
        path: 'chart',
        name: 'chart',
        component: () => import('@/views/chart/index'),
        meta: { title: '图表', icon: 'tree' }
      },
      {
        path: 'table',
        name: 'Table',
        component: () => import('@/views/source/index'),
        meta: { title: '源数据', icon: 'table' }
      }
    ]
  }

]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  {
    path: '/crawler',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'crawler',
        component: () => import('@/views/crawler/index'),
        meta: { title: '采集管理', icon: 'link', roles: ['管理员'] }
      }
    ]
  },
  {
    path: '/predict',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'predict',
        component: () => import('@/views/predict/index'),
        meta: { title: '房价预测', icon: 'link', roles: ['管理员'] }
      }
    ]
  },
  {
    path: '/setting',
    component: Layout,
    redirect: '/setting/source',
    name: 'setting',
    meta: { title: '个人设置', icon: 'el-icon-setting' },
    children: [
      {
        path: 'mima',
        name: 'mima',
        component: () => import('@/views/setting/mima/index'),
        meta: { title: '重置密码', icon: 'form' }
      },
      {
        path: 'info',
        name: 'info',
        component: () => import('@/views/setting/info/index'),
        meta: { title: '个人信息', icon: 'form' }
      }
    ]
  },
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
