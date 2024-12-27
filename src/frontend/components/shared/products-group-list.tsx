'use client';

import React from 'react';
import { cn } from '@/lib/utils';
import { ProductCard, Title } from '../shared';

interface ProductItem {
    id: number;
    name: string;
    price: number;
  }
  

interface Props {
  title: string;
  items: ProductItem[];
  categoryId: number;
  className?: string;
  listClassName?: string;
}

export const ProductsGroupList: React.FC<Props> = ({
  title,
  items,
  listClassName,
  className,
}) => {
  return (
    <div className={className}>
      <Title text={title} size="lg" className="font-extrabold mb-5" />

      <div className={cn('grid grid-cols-3 gap-[50px]', listClassName)}>
        {items.map((product) => (
          <ProductCard
            key={product.id}
            id={product.id}
            name={product.name}
            price={product.price}
          />
        ))}
      </div>
    </div>
  );
};