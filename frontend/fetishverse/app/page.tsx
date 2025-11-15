import { Suspense } from 'react'
import { ProductGrid } from '@/components/product-grid'
import { Hero } from '@/components/hero'
import { CategoryFilter } from '@/components/category-filter'
import { getProducts } from '@/lib/products'

export default async function HomePage() {
  const featuredProducts = await getProducts({ featured: true, limit: 8 })

  return (
    <div className="min-h-screen">
      <Hero />
      
      <section className="container py-12">
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-4">Featured Content</h2>
          <CategoryFilter />
        </div>
        
        <Suspense fallback={<ProductGridSkeleton />}>
          <ProductGrid products={featuredProducts} />
        </Suspense>
      </section>

      <section className="container py-12">
        <h2 className="text-3xl font-bold mb-8">New Releases</h2>
        <Suspense fallback={<ProductGridSkeleton />}>
          <NewReleases />
        </Suspense>
      </section>
    </div>
  )
}

async function NewReleases() {
  const products = await getProducts({ limit: 12, sort: 'newest' })
  return <ProductGrid products={products} />
}

function ProductGridSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {[...Array(8)].map((_, i) => (
        <div key={i} className="animate-pulse">
          <div className="bg-muted h-64 rounded-lg mb-4" />
          <div className="h-4 bg-muted rounded w-3/4 mb-2" />
          <div className="h-4 bg-muted rounded w-1/2" />
        </div>
      ))}
    </div>
  )
}

