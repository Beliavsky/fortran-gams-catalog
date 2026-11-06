program correlation
  use fftpack, only: xcorr
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  integer :: nx, ny, n, pattern, i, j, lag, count
  complex(kind=8), allocatable :: x(:), y(:), reference(:), z(:)
  real(kind=8), allocatable :: r(:), real_reference(:)
  complex(kind=4), allocatable :: xs(:), ys(:), zs(:)
  real(kind=4), allocatable :: rs(:)
  real(kind=8) :: scale, error, max_double, max_single
  count=0; max_double=0; max_single=0
  do nx=1,7
    do ny=1,7
      n=max(nx,ny)
      allocate(x(nx),y(ny),reference(2*n-1),real_reference(2*n-1),xs(nx),ys(ny))
      do pattern=1,3
        do i=1,nx
          x(i)=cmplx(sin(real(2*i+nx,8)),cos(real(i+ny,8)),8)
        end do
        do i=1,ny
          y(i)=cmplx(cos(real(3*i+ny,8)),sin(real(i-nx,8)),8)
        end do
        if(pattern==2)then
          x=0; y=0
          x(nx)=cmplx(2.0_8,-1.0_8,8); y(1)=cmplx(-3.0_8,2.0_8,8)
        else if(pattern==3)then
          x=0
        end if
        reference=0; real_reference=0
        do lag=1-n,n-1
          do j=1,ny
            i=j+lag
            if(i>=1.and.i<=nx)then
              reference(lag+n)=reference(lag+n)+x(i)*conjg(y(j))
              real_reference(lag+n)=real_reference(lag+n)+real(x(i),8)*real(y(j),8)
            end if
          end do
        end do
        z=xcorr(x,y)
        call check_complex(z,reference,2e-12_8,.false.)
        r=xcorr(real(x,8),real(y,8))
        call check_complex(cmplx(r,0.0_8,8),cmplx(real_reference,0.0_8,8),2e-12_8,.false.)
        ! Round inputs before the single-kind reference comparisons.
        xs=cmplx(x,kind=4); ys=cmplx(y,kind=4)
        reference=0; real_reference=0
        do lag=1-n,n-1
          do j=1,ny
            i=j+lag
            if(i>=1.and.i<=nx)then
              reference(lag+n)=reference(lag+n)+cmplx(xs(i),kind=8)*conjg(cmplx(ys(j),kind=8))
              real_reference(lag+n)=real_reference(lag+n)+real(xs(i),8)*real(ys(j),8)
            end if
          end do
        end do
        zs=xcorr(xs,ys)
        call check_complex(cmplx(zs,kind=8),reference,2e-6_8,.true.)
        rs=xcorr(real(xs,4),real(ys,4))
        call check_complex(cmplx(rs,0.0_4,8),cmplx(real_reference,0.0_8,8),2e-6_8,.true.)
      end do
      deallocate(x,y,reference,real_reference,xs,ys)
    end do
  end do
  print '(a,i0)', 'Direct-sum cross-correlation comparisons: ',count
  print '(a,es14.6)', 'Maximum normalized binary64 error: ',max_double
  print '(a,es14.6)', 'Maximum normalized binary32 error: ',max_single
  print '(a)', 'PASS correlation'
contains
  subroutine check_complex(actual,expected,tolerance,single)
    complex(kind=8), intent(in) :: actual(:),expected(:)
    real(kind=8), intent(in) :: tolerance
    logical, intent(in) :: single
    if(size(actual)/=size(expected))error stop 'Wrong output size'
    if(.not.all(ieee_is_finite(real(actual,8))))error stop 'Nonfinite real output'
    if(.not.all(ieee_is_finite(aimag(actual))))error stop 'Nonfinite imaginary output'
    scale=max(1.0_8,maxval(abs(expected)))
    error=maxval(abs(actual-expected))/scale
    if(error>tolerance)then
      print *,nx,ny,pattern,error,tolerance
      error stop 'Cross-correlation differs from direct sums'
    end if
    if(single)then
      max_single=max(max_single,error)
    else
      max_double=max(max_double,error)
    end if
    count=count+1
  end subroutine
end program
