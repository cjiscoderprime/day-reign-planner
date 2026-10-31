
<script lang="ts">
  import { api, type AuthUser } from '#lib/api.ts';

  let { onAuthenticated }: {
    onAuthenticated: (user: AuthUser) => void
  } = $props();

  let mode = $state<'login' | 'register'>('login');

  let name = $state('');
  let email = $state('');
  let password = $state('');
  let error = $state('');
  let submitting = $state(false);

  async function submit(event: SubmitEvent) {
    event.preventDefault();

    if (submitting) return;

    submitting = true;
    error = '';

    try {
      const user = mode === 'login'
        ? await api.login(email, password)
        : await api.register({ name, email, password });

      onAuthenticated(user);
    } catch (err) {
      error = err instanceof Error
        ? err.message
        : 'Authentication failed';
    } finally {
      submitting = false;
    }
  }
</script>

<div class="flex min-h-screen items-center justify-center
            bg-[#F5F0E6] px-4 py-12">

  <div class="w-full max-w-md rounded-2xl
              border border-[#D9C9AE] bg-[#FFFDF8]
              p-8 shadow-xl">

    <div class="mb-8 text-center">
      <div class="text-4xl text-[#C6A052]">🏛️</div>

      <h1 class="mt-2 font-serif text-4xl
                 font-bold tracking-widest text-[#8E2028]">
        DAYREIGN
      </h1>

      <p class="mt-2 text-sm tracking-widest text-[#A18347]">
        COMMAND YOUR DAY
      </p>
    </div>

    <h2 class="mb-6 text-center font-serif
               text-2xl text-[#292524]">
      {mode === 'login'
        ? 'Welcome'
        : 'Begin Your Reign'}
    </h2>

    <form onsubmit={submit} class="space-y-5">

      {#if mode === 'register'}
        <div>
          <label for="auth-name" class="mb-2 block text-sm">
            Name
          </label>
          <input
            id="auth-name"
            bind:value={name}
            required
            maxlength="80"
            autocomplete="name"
            class="w-full rounded-lg border border-[#D9C9AE]
                   bg-white p-3 focus:outline-[#8E2028]"
          />
        </div>
      {/if}

      <div>
        <label for="auth-email" class="mb-2 block text-sm">
          Email address
        </label>
        <input
          id="auth-email"
          type="email"
          bind:value={email}
          required
          autocomplete="email"
          class="w-full rounded-lg border border-[#D9C9AE]
                 bg-white p-3 focus:outline-[#8E2028]"
        />
      </div>

      <div>
        <label for="auth-password" class="mb-2 block text-sm">
          Password
        </label>
        <input
          id="auth-password"
          type="password"
          bind:value={password}
          required
          minlength={mode === 'register' ? 12 : undefined}
          autocomplete={mode === 'login'
            ? 'current-password'
            : 'new-password'}
          class="w-full rounded-lg border border-[#D9C9AE]
                 bg-white p-3 focus:outline-[#8E2028]"
        />

        {#if mode === 'register'}
          <p class="mt-2 text-xs text-[#766C60]">
            Use at least 12 characters.
          </p>
        {/if}
      </div>

      {#if error}
        <p role="alert" class="text-sm text-red-700">
          {error}
        </p>
      {/if}

      <button
        type="submit"
        disabled={submitting}
        class="w-full rounded-lg bg-[#8E2028] px-5 py-3
               font-semibold text-white transition
               hover:bg-[#741920] disabled:opacity-50"
      >
        {submitting
          ? 'Please wait...'
          : mode === 'login'
            ? 'Enter DayReign'
            : 'Create Account'}
      </button>
    </form>

    <div class="mt-6 text-center text-sm">
      <button
        type="button"
        class="font-medium text-[#8E2028] underline"
        onclick={() => {
          mode = mode === 'login' ? 'register' : 'login';
          error = '';
        }}
      >
        {mode === 'login'
          ? 'Create a new account'
          : 'Already have an account? Sign in'}
      </button>
    </div>

  </div>
</div>
