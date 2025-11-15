'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { ImageIcon, Loader2 } from 'lucide-react'
import { generateImage } from '@/lib/api'
import { useToast } from '@/hooks/use-toast'

const imageSchema = z.object({
  prompt: z.string().min(10, 'Prompt must be at least 10 characters'),
  negative_prompt: z.string().optional(),
  width: z.number().min(256).max(2048).default(1024),
  height: z.number().min(256).max(2048).default(1024),
  steps: z.number().min(10).max(100).default(30),
  guidance_scale: z.number().min(1).max(20).default(7.5),
})

type ImageFormData = z.infer<typeof imageSchema>

export default function ImageGenerationPage() {
  const [generating, setGenerating] = useState(false)
  const [progress, setProgress] = useState(0)
  const [result, setResult] = useState<string | null>(null)
  const { toast } = useToast()

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch
  } = useForm<ImageFormData>({
    resolver: zodResolver(imageSchema),
    defaultValues: {
      width: 1024,
      height: 1024,
      steps: 30,
      guidance_scale: 7.5,
    }
  })

  const onSubmit = async (data: ImageFormData) => {
    setGenerating(true)
    setProgress(0)
    setResult(null)

    try {
      // Simulate progress updates (in real app, use WebSocket)
      const progressInterval = setInterval(() => {
        setProgress(prev => Math.min(prev + 10, 90))
      }, 500)

      const response = await generateImage(data)

      clearInterval(progressInterval)
      setProgress(100)
      setResult(response.image_url)

      toast({
        title: 'Success!',
        description: 'Image generated successfully',
      })
    } catch (error) {
      toast({
        title: 'Error',
        description: error instanceof Error ? error.message : 'Failed to generate image',
        variant: 'destructive',
      })
    } finally {
      setGenerating(false)
    }
  }

  return (
    <div className="container py-8 max-w-6xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Image Generation</h1>
        <p className="text-muted-foreground">
          Generate high-quality images using AI. No content filters, complete control.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card>
          <CardHeader>
            <CardTitle>Generation Settings</CardTitle>
            <CardDescription>Configure your image generation parameters</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="prompt">Prompt *</Label>
                <Textarea
                  id="prompt"
                  {...register('prompt')}
                  placeholder="Describe the image you want to generate..."
                  rows={4}
                />
                {errors.prompt && (
                  <p className="text-sm text-destructive">{errors.prompt.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="negative_prompt">Negative Prompt</Label>
                <Textarea
                  id="negative_prompt"
                  {...register('negative_prompt')}
                  placeholder="What to avoid in the image..."
                  rows={2}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="width">Width</Label>
                  <Input
                    id="width"
                    type="number"
                    {...register('width', { valueAsNumber: true })}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="height">Height</Label>
                  <Input
                    id="height"
                    type="number"
                    {...register('height', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="steps">Steps</Label>
                  <Input
                    id="steps"
                    type="number"
                    {...register('steps', { valueAsNumber: true })}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="guidance_scale">Guidance Scale</Label>
                  <Input
                    id="guidance_scale"
                    type="number"
                    step="0.1"
                    {...register('guidance_scale', { valueAsNumber: true })}
                  />
                </div>
              </div>

              {generating && (
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span>Generating...</span>
                    <span>{progress}%</span>
                  </div>
                  <Progress value={progress} />
                </div>
              )}

              <Button
                type="submit"
                disabled={generating}
                className="w-full"
                size="lg"
              >
                {generating ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Generating...
                  </>
                ) : (
                  <>
                    <ImageIcon className="w-4 h-4 mr-2" />
                    Generate Image
                  </>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Preview</CardTitle>
            <CardDescription>Your generated image will appear here</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="aspect-square bg-muted rounded-lg flex items-center justify-center">
              {result ? (
                <img
                  src={result}
                  alt="Generated"
                  className="w-full h-full object-contain rounded-lg"
                />
              ) : (
                <div className="text-center text-muted-foreground">
                  <ImageIcon className="w-16 h-16 mx-auto mb-4 opacity-50" />
                  <p>No image generated yet</p>
                </div>
              )}
            </div>

            {result && (
              <div className="mt-4 flex gap-2">
                <Button
                  variant="outline"
                  onClick={() => window.open(result, '_blank')}
                  className="flex-1"
                >
                  Download
                </Button>
                <Button
                  variant="outline"
                  onClick={() => setResult(null)}
                >
                  Clear
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

