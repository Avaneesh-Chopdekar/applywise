import type { PropsWithChildren } from "react";
import { ChakraProvider, defaultSystem } from "@chakra-ui/react";
import { ThemeProvider } from "next-themes";
import { QueryClientProvider, QueryClient } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

const queryClient = new QueryClient();

export default function Provider({ children }: PropsWithChildren) {
  return (
    <QueryClientProvider client={queryClient}>
      <ChakraProvider value={defaultSystem}>
        <ThemeProvider attribute="class" disableTransitionOnChange>
          {children}
          <ReactQueryDevtools initialIsOpen={false} />
        </ThemeProvider>
      </ChakraProvider>
    </QueryClientProvider>
  );
}
