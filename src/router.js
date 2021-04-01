import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '@/components/pages/Home.vue';
import BaseLayout from '@/components/layouts/BaseLayout.vue';

import Host from '@/components/pages/host/Host.vue';
import SessionDetail from '@/components/pages/host/SessionDetail.vue';
import FobbitDetail from '@/components/pages/host/FobbitDetail.vue';
import Scores from '@/components/pages/host/Scores.vue';
import ScoreBoard from '@/components/pages/host/ScoreBoard.vue';

import Play from '@/components/pages/play/Play.vue';
import SelectSession from '@/components/pages/play/SelectSession.vue';

Vue.use(VueRouter);

const routes = [
  // Home
  {
    path: '',
    component: BaseLayout,
    meta: {
      title: 'Fobbage',

    },
    children: [
      {
        path: '/',
        component: Home,
        name: 'home',
      },
      // Select
      {
        path: 'play',
        component: BaseLayout,
        children: [
          {
            path: 'select',
            component: SelectSession,
            name: 'join-session',
          },
          {
            path: ':id(\\d+)?',
            component: Play,
            props: (route) => ({ sessionId: Number(route.params.id) }),
          },
        ],
      },
      // Host
      {
        path: 'host',
        component: Host,
        name: 'host',
      },
      {
        path: 'host/:sessionId',
        component: SessionDetail,
        props: (route) => ({ sessionId: Number(route.params.sessionId) }),
        children:
        [
          {
            path: '',
            component: FobbitDetail,
            name: 'session-detail',
            children:
            [
              {
                path: 'scores',
                component: Scores,
                name: 'scores',
              },
            ],
          },
          {
            path: 'scoreboard',
            component: ScoreBoard,
            name: 'scoreboard',
          },
        ],
      },
    ],
  },
  // login  pages
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "login" */ '@/components/pages/Login.vue'),
    meta: {
      title: 'Fobbage - Login',
      skipAuth: true,
    },
  },
  // login  pages
  {
    path: '/logout',
    name: 'logout',
    component: () => import(/* webpackChunkName: "login" */ '@/components/pages/Logout.vue'),
    meta: {
      title: 'Fobbage - Logout',
      skipAuth: true,
    },
  },
  // register  pages
  {
    path: '/register',
    name: 'register',
    component: () => import(/* webpackChunkName: "login" */ '@/components/pages/Register.vue'),
    meta: {
      title: 'Fobbage - Register',
      skipAuth: true,
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
  if (to.matched.some((route) => !route.meta.skipAuth)) {
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
