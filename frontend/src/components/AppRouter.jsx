import { Navigate, Route, Routes } from "react-router-dom";
import { privateRoutes, publicRoutes, RouteNames } from "../router";
import useUserStore from "../store/useUserStore";
import React from "react";

const AppRouter = () => {
  const isAuth = useUserStore((state) => state.isAuth);
  return isAuth ? (
    <Routes>
      {privateRoutes.map((route) => (
        <Route
          path={route.path}
          key={route.path}
          element={<route.component />}
        />
      ))}
      <Route path="*" element={<Navigate to={RouteNames.MAIN} replace />} />
    </Routes>
  ) : (
    <Routes>
      {publicRoutes.map((route) => (
        <Route
          path={route.path}
          key={route.path}
          element={<route.component />}
        />
      ))}
      <Route path="*" element={<Navigate to={RouteNames.LOGIN} replace />} />
    </Routes>
  );
};

export default AppRouter;
