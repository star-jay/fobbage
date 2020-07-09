import Vue from 'vue';
import VueRouter from 'vue-router';
import Play from '@/views/Play.vue';
import Home from '@/views/Home.vue';
import Quizlist from '@/views/Quizlist.vue';

Vue.use(VueRouter);

const routes = [
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
      },
      {
        path: '/:id(\\d+)?',
        component: Play,
        props: (route) => ({ id: Number(route.params.id) }),
      },
    ],
  },
  // login  pages
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "login" */ './views/Login.vue'),
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
    meta: {
      title: 'Fobbage - Register',
    },
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

const isAuthenticated = () => localStorage.getItem('accessToken');

router.beforeEach(async (to, from, next) => {
  if (to.matched.some((route) => route.meta.requiresAuth)) {
    // Route is protected
    if (!isAuthenticated()) {
      // Not authenticated. Go to login page.
      if (from.path !== 'login') {
        next({
          name: 'login',
          params: { nextUrl: to.fullPath },
        });
      }
    } else {
      // Authenticated, go ahead with the navigation.
      next();
    }
  } else {
    // Route is not protected
    next();
  }
});

export default router;
