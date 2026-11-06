! GAMS J1a1: fftpack::fft(real64) checked against an independent direct DFT.
program real_dft
 use iso_fortran_env, only: real64
 use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
 use fftpack, only: fft
 implicit none
 integer,parameter :: sizes(*)=[1,2,3,4,5,7,8,9,10,16,17]
 integer :: k,n,i,j,mode,dim,count
 real(real64),allocatable :: x(:)
 complex(real64),allocatable :: z(:),want(:)
 real(real64) :: angle,error,maximum,pi
 maximum=0;count=0;pi=acos(-1._real64)
 do k=1,size(sizes)
  n=sizes(k)
  allocate(x(n))
  do i=1,n
   x(i)=cos(0.4_real64*i)-0.1_real64*i
  end do
  do mode=1,3
   select case(mode)
   case(1);dim=n;z=fft(x)
   case(2);dim=n+3;z=fft(x,dim)
   case(3);dim=max(1,n-2);z=fft(x,dim)
   end select
   if(size(z)/=dim) error stop 'DFT output size'
   allocate(want(dim));want=0
   do j=0,dim-1
    do i=0,min(n,dim)-1
     angle=-2*pi*j*i/dim
     want(j+1)=want(j+1)+x(i+1)*cmplx(cos(angle),sin(angle),kind=real64)
    end do
   end do
   if(.not.all(ieee_is_finite(real(z))) .or. .not.all(ieee_is_finite(aimag(z)))) error stop 'nonfinite DFT'
   error=maxval(abs(z-want))/max(1._real64,maxval(abs(want)))
   maximum=max(maximum,error)
   if(error>5.e-12_real64) error stop 'DFT mismatch'
   count=count+1
   deallocate(want,z)
  end do
  deallocate(x)
 end do
 print '(a,i0)', 'Direct real-input DFT comparisons: ',count
 print '(a,es14.6)', 'Maximum normalized error: ',maximum
 print '(a)', 'PASS real_dft'
end program
