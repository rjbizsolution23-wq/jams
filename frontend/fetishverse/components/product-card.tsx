'use client'

import Image from 'next/image'
import Link from 'next/link'
import { ShoppingCart, Heart, Eye } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { useCart } from '@/store/cart-store'
import { formatPrice } from '@/lib/utils'

interface ProductCardProps {
  product: {
    id: string
    name: string
    slug: string
    price: number
    preview_image_url: string | null
    category: string | null
    rating_average: number
    rating_count: number
    is_featured?: boolean
  }
}

export function ProductCard({ product }: ProductCardProps) {
  const { addToCart } = useCart()

  return (
    <div className="group relative bg-card rounded-lg border overflow-hidden hover:shadow-lg transition-shadow">
      <Link href={`/products/${product.slug}`}>
        <div className="relative aspect-square overflow-hidden bg-muted">
          {product.preview_image_url ? (
            <Image
              src={product.preview_image_url}
              alt={product.name}
              fill
              className="object-cover group-hover:scale-105 transition-transform"
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 25vw"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <Eye className="w-12 h-12 text-muted-foreground" />
            </div>
          )}
          
          {product.is_featured && (
            <Badge className="absolute top-2 left-2">Featured</Badge>
          )}
          
          <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors" />
        </div>
      </Link>

      <div className="p-4">
        <div className="mb-2">
          {product.category && (
            <Badge variant="secondary" className="text-xs mb-1">
              {product.category}
            </Badge>
          )}
          <Link href={`/products/${product.slug}`}>
            <h3 className="font-semibold line-clamp-2 hover:text-primary transition-colors">
              {product.name}
            </h3>
          </Link>
        </div>

        <div className="flex items-center justify-between mb-3">
          <div>
            <p className="text-2xl font-bold">{formatPrice(product.price)}</p>
            {product.rating_count > 0 && (
              <p className="text-sm text-muted-foreground">
                ⭐ {product.rating_average.toFixed(1)} ({product.rating_count})
              </p>
            )}
          </div>
        </div>

        <div className="flex gap-2">
          <Button
            onClick={() => addToCart(product)}
            className="flex-1"
            size="sm"
          >
            <ShoppingCart className="w-4 h-4 mr-2" />
            Add to Cart
          </Button>
          <Button variant="outline" size="sm">
            <Heart className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  )
}

