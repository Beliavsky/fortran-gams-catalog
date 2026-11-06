! GAMS I2a2; scalar advection interface checks.
! Upstream pin: 008d4921ea46878a97a96c8b8daa399a2e7b9078
program check_advection
  implicit none
  interface
    subroutine rp1_ptwise(ne,na,nw,ql,qr,al,ar,w,s,am,ap)
      integer, intent(in) :: ne,na,nw
      real(kind=8), intent(inout) :: ql(ne),qr(ne),al(na),ar(na)
      real(kind=8), intent(inout) :: w(ne,nw),s(nw),am(ne),ap(ne)
    end subroutine
  end interface
  real(kind=8) :: u
  common /cparam/ u
  real(kind=8) :: ql(1),qr(1),al(1),ar(1),w(1,1),s(1),am(1),ap(1)
  real(kind=8), parameter :: speeds(3)=[-2d0,0d0,3d0]
  real(kind=8), parameter :: left(3)=[1d0,-1d0,2d0],right(3)=[4d0,2d0,2d0]
  real(kind=8) :: flux,err,maxerr,tol
  integer :: i,j
  maxerr=0d0; al=0d0; ar=0d0
  do i=1,size(speeds)
    u=speeds(i)
    do j=1,size(left)
      ql=left(j); qr=right(j); w=0d0; s=0d0; am=0d0; ap=0d0
      call rp1_ptwise(1,1,1,ql,qr,al,ar,w,s,am,ap)
      if(u>=0d0)then
        flux=u*left(j)
      else
        flux=u*right(j)
      endif
      err=max(abs(u*left(j)+am(1)-flux),abs(u*right(j)-ap(1)-flux), &
              abs(am(1)+ap(1)-u*(right(j)-left(j))), &
              abs(w(1,1)-(right(j)-left(j))),abs(s(1)-u))
      tol=2d-13*max(1d0,abs(flux),abs(u*left(j)),abs(u*right(j)))
      if(.not.(err<=tol))error stop 'advection flux/speed/jump check failed'
      maxerr=max(maxerr,err)
    enddo
  enddo
  print '(a,es12.4)','Maximum absolute error: ',maxerr
  print '(a)','PASS advection: 9 positive/negative/zero-speed and state cases'
end program check_advection
