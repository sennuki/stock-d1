// @ts-check
import { defineConfig } from 'astro/config';

// Cloudflare Pagesで静的サイトとして配信する場合は、
// アダプターを使用せずに標準的なビルドを行う構成も検討します。
// ただし、Functionsを利用し続けるため、ビルド設定のみを調整します。

// https://astro.build/config
export default defineConfig({
  output: 'static',
  // CloudflareアダプターがASSETSバインディングでエラーを起こす場合、
  // 一時的にアダプターを外して静的ビルドを行い、Pages側で配信を制御します。
});
