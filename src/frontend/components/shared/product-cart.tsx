import Link from 'next/link'
import React from 'react'
import { Button } from '../ui'
import { Title } from '../shared' 

import { Plus } from 'lucide-react';

interface Props {
    id: number;
    name: string;
    price: number;
    className?: string;
}

export const ProductCard: React.FC<Props> = ({ 
    id, 
    name, 
    price, 
    className 
}) => {
    return (
      <div className={className}>
        <Link href={`/product/${id}`}>
            <div className='felx justify-center p-6 bg-secondary rounded-lg h-[260px]'>
                <img className="w-[215px] h-[215px]" src='https://img.mvideo.ru/Big/40079746bb.jpg' alt={name} />
            </div>

            <Title text={name} size="sm" className="mb-1 mt-3 font-bold" />

            <div className="flex justify-between items-center mt-4">
                <span className="text-[20px]">
                    <b>{price} ₽</b>
                </span>

                <Button variant="secondary" className="text-base font-bold">
                    <Plus size={20} className="mr-1" />
                    Добавить
                </Button>
            </div>
        </Link>
      </div>
    )
}