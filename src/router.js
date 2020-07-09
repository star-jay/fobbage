import Vue from 'vue';
import Router from 'vue-router';
import store from '@/store';
import Play from '@/views/Play.vue';
import Home from '@/views/Home.vue';
import Quizlist from '@/views/Quizlist.vue';


Vue.use(Router);

const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters.isAuthenticated) {
    next();
    return;
  }
  next('/');
};

const ifAuthenticated = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    next();
    return;
  }
  next({ name: 'login' });
};

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    // Home
    {
      path: '/',
      component: Home,
      meta: {
        title: 'Fobbage',
      },
      children: [
        // pick a quiz
        {
          path: '',
          component: Quizlist,
          beforeEnter: ifAuthenticated,
        },
        {
          path: '/:id(\\d+)?',
          component: Play,
          beforeEnter: ifAuthenticated,
          props: route => ({ id: Number(route.params.id) }),
        },
      ],
    },
    // login  pages
    {
      path: '/login',
      name: 'login',
      component: () => import(/* webpackChunkName: "login" */ './views/Login.vue'),
      beforeEnter: ifNotAuthenticated,
      meta: {
        title: 'Fobbage - Login',
      },
    },
    // login  pages
    {
      path: '/logout',
      name: 'logout',
      component: () => import(/* webpackChunkName: "login" */ './views/Logout.vue'),
      meta: {
        title: 'Fobbage - Logout',
      },
    },
    // register  pages
    {
      path: '/register',
      name: 'register',
      component: () => import(/* webpackChunkName: "login" */ './views/Register.vue'),
      beforeEnter: ifNotAuthenticated,
      meta: {
        title: 'Fobbage - Register',
      },
    },

  ],
});
