'use client'

import React, { useState } from "react";
import { Button } from "@/components/ui";
import { Container, LoginModal } from "../shared";
import Link from "next/link";
import { ArrowRight, User, ShoppingCart } from "lucide-react";

export const Header: React.FC = () => {
  const [isModalOpen, setModalOpen] = useState(false);

  const toggleModal = () => setModalOpen(!isModalOpen);

  return (
    <header className="sticky top-0 bg-white shadow-lg shadow-black/5 z-10">
      <Container className="flex items-center justify-between py-8">
            {/* Левая часть */}
            <Link href="/">
              <div className="flex items-center gap-4">
                <div className="text-6xl font-extrabold text-blue-600">MAE</div>
                <div>
                  <h1 className="text-3xl uppercase font-black">- store</h1>
                  <p className="text-sm text-gray-400 leading-3">интернет-магазин техники</p>
                </div>
              </div>
            </Link>

            {/* Правая часть */}
            <div className="flex items-center gap-3">
              <Button
                variant={"outline"}
                className="flex items-center gap-1"
                onClick={toggleModal}
              >
                <User size={16} />
                Войти
              </Button>

              <div>
                <Button className="group relative">
                  <b>520 ₽</b>
                  <span className="h-full w-[1px] bg-white/30 mx-3" />
                  <div className="flex items-center gap-2 transition duration-300 group-hover:opacity-0">
                    <ShoppingCart size={16} className="relative" strokeWidth={2} />
                    <b>3</b>
                  </div>
                  <ArrowRight
                    size={20}
                    className="absolute right-5 transition duration -translate-x-2 opacity-0 group-hover:opacity-100 group-hover:translate-x-0"
                  />
                </Button>
              </div>
            </div>
          </Container>

      {/* Подключаем модальное окно */}
      <LoginModal isOpen={isModalOpen} onClose={toggleModal} />
    </header>
  );
};
