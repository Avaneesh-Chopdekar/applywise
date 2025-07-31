import { createRootRoute, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";
import Provider from "@/components/providers";

export const Route = createRootRoute({
  component: () => (
    <Provider>
      {/* Navbar Component */}
      <Outlet />
      <TanStackRouterDevtools />
    </Provider>
  ),
});
